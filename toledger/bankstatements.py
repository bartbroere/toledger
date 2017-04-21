"""bankstatements.py
Contains metadata for parsing input files
"""

from time import strftime, strptime
import hashlib

#2017-04-21 13:21 Market
#    Assets:Bitstamp              10 BTC @@ $5000.00
#    Assets:Bitstamp

#2017-04-21 14:21 Deposit
#    Assets:Bitstamp              10 BTC
#    Equity:Unspecified

def bitstamp_net_parse(header, entry, format, a):
    parsed = {"meta": {}}
    for name, field in bitstamp_net["fields"].items():
        if field == "meta": 
            parsed["meta"][name] = entry[header.index(name)]
        else: 
            parsed[field] = entry[header.index(name)]
    if parsed["name"] in ["Deposit", "Withdrawal"]:
        if parsed["name"] == "Withdrawal": 
            parsed["direction"] = "-"
    elif parsed["name"] == "Market":
        if parsed["meta"]["Sub Type"] == "Sell":
            parsed["direction"] = "-"
    elif parsed["name"] == "Sub Account Transfer":
        if parsed["value"] == "Addition":
            parsed["direction"] = "-"
            parsed["destination"] = parsed["meta"]["Account"].replace(
                " ", "")
    else:
        raise NotImplementedError("This transaction type is unknown")
    parsed["amount"] = parsed.get("direction", "")+parsed["amount"]
    if a["--hash"]: 
        parsed["hash"] = hashlib.sha256(" ".join(entry).encode(
                             "utf-8")).hexdigest()
    parsed["date"] = strftime("%Y-%m-%d %H:%M", 
                              strptime(parsed["date"], 
                              "%b. %d, %Y, %I:%M %p"))
    return parsed

def bitstamp_net_write(output, a, **data):
    account = a["--name"] if a["--name"] else "Assets:Bitstamp"
    source = a["--from"] if a["--from"] else "Assets:Unspecified"
    output.write("\n")
    output.write(data["date"]+" "+data["name"])
    if data["name"] in ["Deposit", "Withdrawal"]:
        output.write("\n\t"+account+"\t"+data["amount"])
        output.write("\n\t"+source+"\n")
    elif data["name"] == "Market":
        output.write("\n\t"+account+"\t"+
                     data["amount"]+" @@ "+data["value"])
        output.write("\n\t"+account+"\n")
    elif data["name"] == "Sub Account Transfer":
        output.write("\n\t"+account+"\t"+data["amount"])
        output.write("\n\t"+account+":"+data["destination"]+"\n")
    for metakey, metavalue in data["meta"].items():
        output.write("\t  ; "+metakey.replace(" ", "")+": "+metavalue+"\n")
    if "hash" in data:
        output.write("\t  ; hash: "+data["hash"]+"\n")
    output.write("\n")
    return

bitstamp_net = {"fields": {"Type": "name",
                           "Datetime": "date",
                           "Account": "meta",
                           "Amount": "amount",
                           "Value": "value",
                           "Rate": "meta",
                           "Fee": "meta",
                           "Sub Type": "meta"},
                "interpretation": {}, #handled by bitstamp_net_parse
                "properties": {"quotechar": "\"",
                               "delimiter": ","},
                "parse": bitstamp_net_parse,
                "write": bitstamp_net_write}

ing_nl = {"fields": {"Datum": "date",
                     "Naam / Omschrijving": "name",
                     "Rekening": "source",
                     "Tegenrekening": "destination",
                     "Code": "meta",
                     "Af Bij": "direction",
                     "Bedrag (EUR)": "amount",
                     "MutatieSoort": "meta",
                     "Mededelingen": "meta"},
          "interpretation": {"directionout": "Af",
                             "currency": {"symbol": u"\u20ac", 
                                          #TODO fix unicode issue
                                          "code": "EUR"},
                             "separators": {"thousandseparator": ".",
                                            "decimalseparator": ","},
                             "dateformat": "%Y%m%d"},
          "properties": {"quotechar": "\"",
                         "delimiter": ","},
          "type": "default"}

kraken_com = {"group_by": "refid",
              "fields": {"time": "date",
                         "refid": "name",
                         "txid": "source",
                         "amount": "amount",
                         "type": "meta",
                         "aclass": "meta",
                         "fee": "meta",
                         "balance": "balance"},
              "interpretation": {},
              "properties": {}}
