# ToLedger
ToLedger originated as a personal project to convert my bank statements 
to the open source [ledger](http://ledger-cli.org/) format. I have made 
some changes to make it more generally applicable, allowing for other 
banks to be added.

Currently this library is only known to work with the export files of
ING Bank (NL), but extending it for similar CSV exports should be trivial.

```
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
                 Default Equity:[Unspecified | IBAN]
  --to=<to>      Account to send transactions to. 
                 Default Expenses:[Unspecified | IBAN]
  --name=<name>  Account name. Default Assets:[IBAN]
  -c --code      Use the currency code, e.g. EUR
  -s --symbol    Use the currency symbol, e.g. €  
  -h --help      Show the usage guidelines.
```

## Installation
Apart from downloading this repository, you can install the latest 
release with ``pip install toledger``

## Contributing
If you wish to contribute to this project, here's a feature wishlist:

+ Add different formats for different banks 
  (see toledger/bankstatements.py)
+ Interactive mode, manually adding and changing transaction details
+ Smart transaction labeling, based on specification files or existing 
  Ledger files
+ Checking the output file for duplicates
+ Convert to using a Ledger library for Python, instead of writing 
  directly to files (better and more output formatting options)
+ Save the meta information in the output file
+ Python 2 compatibility
+ Unit tests
+ Any other suggestions are also welcome, especially if they improve 
  extensibility and compatibility

There are also some design conventions:

+ [PEP 8](https://www.python.org/dev/peps/pep-0008/) (within reason)
+ All options should be reachable from the command line, using 
  [docopt](http://docopt.org)
+ [stdin and stdout compatibility](https://docs.python.org/3/library/sys.html#sys.stdin)
+ Error handling with 
  [built-in exceptions](https://docs.python.org/3.6/library/exceptions.html) 
  (with custom messages)