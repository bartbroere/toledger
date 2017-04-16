"""bankstatements.py
Contains metadata for parsing input files
"""

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
                         "delimiter": ","}}