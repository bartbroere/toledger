"""ToLedger: Bank statements to ledger format

Usage: 
  toledger.py <format> [options] 
  toledger.py <format> [options] <input>
  toledger.py <format> [options] <input> <output>
  toledger.py (-h | --help)

Options:
  -a --append    Append to the output file if it exists.
  -b --balance   Ensure that all output is balanced.
                 Choose this option if the output must be a
                 standalone ledger file. These files should always
                 have a balance of 0 to be valid.
  --from=<from>  Account to get balances from. 
  --to=<to>      Account to send transactions to. 
  --name=<name>  Account name.
  --hash         Save a hash of the transaction for duplicate removal
  -c --code      Use the currency code, e.g. EUR
  -s --symbol    Use the currency symbol, e.g. €  
  -h --help      Show the usage guidelines.

"""
from docopt import docopt
from sys import stdin, stdout
import csv
import bankstatements
from time import strftime, strptime
import hashlib

def main(a):
    with open(a["<input>"], "r") as inputfile:
        input = csv.reader(inputfile, **properties(a["<format>"]))
        filemode = "a" if a["--append"] else "w"
        if not a["<output>"]: outputlocation = stdout
        else: outputlocation = open(a["<output>"], filemode, encoding="utf8")
        with outputlocation as output:
            i = 0
            for inputentry in input:
                if i == 0:
                    header = inputentry
                else:
                    parsedentry = parse(header, inputentry, a["<format>"])
                    # TODO: Interactive mode
                    write(output, **parsedentry)
                i += 1
    return 0

def parse(header, entry, format):
    # TODO: Smart transaction labeling
    if "parse" in specification(a["<format>"]).keys():
        return specification(format)["parse"](header, entry, format, a)
    parsed = {"meta": {}}
    for name, field in specification(format)["fields"].items():
        if field == "meta": parsed["meta"][name] = entry[header.index(name)]
        else: parsed[field] = entry[header.index(name)]
    for name, field in specification(format)["interpretation"].items():
        if name == "directionout":
            parsed["direction"] = "-" if parsed["direction"] == field else ""
        elif name == "currency":
            if a["--code"]: 
                parsed["amount"] = " ".join([parsed["amount"], field["code"]])
            elif a["--symbol"]: 
                parsed["amount"] = " ".join([field["symbol"], parsed["amount"]])
        elif name == "separators":
            parsed["amount"] = parsed["amount"].replace(
                field["thousandseparator"], "")
            parsed["amount"] = parsed["amount"].replace(
                field["decimalseparator"], ".")
        elif name == "dateformat":
            parsed["date"] = strftime("%Y-%m-%d", 
                                      strptime(parsed["date"], 
                                      field))
    if a["--hash"]: 
        parsed["hash"] = hashlib.sha256(" ".join(entry)).hexdigest()
    return parsed

def specification(format):
    try: return getattr(bankstatements, format)
    except: raise NotImplementedError("The specified format does not exist")

def properties(format): return specification(format)["properties"]

def write(output, **data):
    if "write" in specification(a["<format>"]).keys():
        return specification(a["<format>"])["write"](output, a, **data)
    output.write("\n")
    output.write(data["date"]+" "+data["name"])
    output.write("\n\t")
    if data.get("direction", "") == "-":
        output.write("Expenses:"+data.get("destination", "Unspecified")+
                     " "+"\n\t")
    else:
        output.write("Equity:"+data.get("destination", "Unspecified")+
                     " "+"\n\t")
    output.write("Assets:"+data.get("source", "Unspecified")+"\t"+
                 data.get("direction", "Unspecified")+
                 data.get("amount", "Unspecified")+"\n")
    for metakey, metavalue in data["meta"].items():
        output.write("\t  ; "+metakey.replace(" ", "")+": "+metavalue+"\n")
    if "hash" in data:
        output.write("\t  ; hash: "+data["hash"]+"\n")
    output.write("\n")
    return

if __name__ == '__main__':
    a = docopt(__doc__, version='ToLedger 2017.04.21')
    main(a)
