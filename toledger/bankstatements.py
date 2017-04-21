"""bankstatements.py
Contains metadata for parsing input files
"""

#2017-04-21 13:21 Market
#    Assets:Bitstamp              10 BTC @@ $5000.00
#    Assets:Bitstamp

#2017-04-21 14:21 Deposit
#    Assets:Bitstamp              10 BTC
#    Equity:Unspecified

bitstamp_net = {"transactiontypes": "Type",
                "Withdrawal": {},
                "Market": {},
                "Sub Account Transfer": {},
                "Deposit": {}}

bitstamp_net = {"fields": {"Type": ["name", "direction"],
                           "Datetime": "date",
                           "Account": "meta",
                           "Amount": "amount",
                           "Value": "value",
                           "Rate": "meta",
                           "Fee": "meta",
                           "Sub Type": "direction"},
                "interpretation": {"byfield": "Type",
                                   "fields": {"Market": "assetconv",
                                              "Deposit": "default",
                                              "Withdrawal": "default",
                                              "Sub Account Transfer": "subaccount"}
                                   "directionout": ["Sell", "Withdrawal"],
                                   "dateformat": ""},
                "properties": {"quotechar": "\"",
                               "delimiter": ","}}

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
                             "currency": {"symbol": u"\u20ac", #TODO fix unicode issue
                                          "code": "EUR"},
                             "separators": {"thousandseparator": ".",
                                            "decimalseparator": ","},
                             "dateformat": "%Y%m%d"},
          "properties": {"quotechar": "\"",
                         "delimiter": ","},
          "type": "default"}

kraken_com = {"group_by": "refid"
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