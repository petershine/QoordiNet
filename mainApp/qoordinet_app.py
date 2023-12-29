from ._shared.managers.baseapp import BaseApp

import pandas as pd


droppedColumnKeys = ['Exchange Quantity',
                     'Exchange Currency', 
                     'Exchange Rate',
                     'Settlement Date',
                     'Currency',
                     'Accrued Interest',
                     'Security Description',
                     'Security Type',
                     'Price',
                     'Commission',
                     'Fees',
                     ]

runDateColumnKey = 'Run Date'
accountColumnKey = 'Account'
typeColumnKey = 'Type'
symbolColumnKey = 'Symbol'
actionColumnKey = 'Action'
amountColumnKey = 'Amount'
premiumColumnKey = 'Premium'
quantityColumnKey = 'Quantity'
dividendColumnKey = 'Dividend'

newlyInsertedColumns = [typeColumnKey, 
                        premiumColumnKey, 
                        dividendColumnKey,
                        ]

rearrangedColumns = [runDateColumnKey, 
                     accountColumnKey, 
                     typeColumnKey, 
                     symbolColumnKey, 
                     actionColumnKey, 
                     premiumColumnKey, 
                     dividendColumnKey, 
                     amountColumnKey, 
                     quantityColumnKey,
                     ]

aux_debitColumnKey = 'aux_debit'
aux_tickerColumnKey = 'aux_ticker'

droppableAuxColumns = [aux_debitColumnKey,
                       aux_tickerColumnKey,
                       ]

replacementHash = {'YOU SOLD OPENING TRANSACTION' : 'OPENING',
                   'YOU SOLD CLOSING TRANSACTION' : 'CLOSING',
                   'YOU BOUGHT OPENING TRANSACTION' : 'OPENING',
                   'YOU BOUGHT CLOSING TRANSACTION' : 'CLOSING',
                   'YOU BOUGHT' : '',
                   'YOU SOLD' : '',
                   '\(100 SHS\)' : '',
                   '\(Margin\)' : '',
                   '\(Cash\)' : '',
                   }

renamedColumnsHash = {runDateColumnKey : 'Date',
                      symbolColumnKey : 'Ticker',
                      actionColumnKey : 'Note',
                      amountColumnKey : 'Activity',
                      quantityColumnKey : 'Share',
                      }


class QoordiNetAppManager(BaseApp):
    def process_data(self, tab_separated):
        rows = tab_separated.strip().split("\n")
        processed_data = [row.split("\t") for row in rows]
        return processed_data
    

    def html_table(self, csv_file, styleClasses: str):
        df = pd.read_csv(csv_file.file, skiprows=4, header=0)

        df = df.drop(columns=droppedColumnKeys)

        mainKeyMask = df[runDateColumnKey].apply(self.is_date)
        actionKeyMask = df[actionColumnKey].apply(self.without_substring)
        amountKeyMask = df[amountColumnKey].apply(self.is_not_zero)
        df = df[mainKeyMask]
        df = df[actionKeyMask]
        df = df[amountKeyMask]

    
        df[newlyInsertedColumns] = ''
        df = df[rearrangedColumns]

        is_option = (df[actionColumnKey].str.contains('CALL', case=False) | df[actionColumnKey].str.contains('PUT', case=False))
        df.loc[is_option, typeColumnKey] = 'OPTION'
        df.loc[is_option, premiumColumnKey] = df.loc[is_option, amountColumnKey]
        df.loc[is_option, amountColumnKey] = ''
        df.loc[is_option, quantityColumnKey] = ''

        df[aux_tickerColumnKey] = df[symbolColumnKey].str.extract(r'-([A-Z]+)').fillna('')
        df.loc[is_option, symbolColumnKey] = df.loc[is_option, aux_tickerColumnKey]

        is_dividend = (df[actionColumnKey].str.contains('DIVIDEND', case=False))
        df.loc[is_dividend, typeColumnKey] = 'dividend'
        df.loc[is_dividend, dividendColumnKey] = df.loc[is_dividend, amountColumnKey]
        df.loc[is_dividend, amountColumnKey] = ''
        df.loc[is_dividend, quantityColumnKey] = ''

        is_debit = (df[actionColumnKey].str.contains('DEBIT', case=False))
        df.loc[is_debit, quantityColumnKey] = ''

        is_invested = (df[amountColumnKey] != '') & (df[quantityColumnKey] != '')
        df.loc[is_invested, typeColumnKey] = 'Invested'

        df[aux_debitColumnKey] = df[actionColumnKey].str.contains('DEBIT', case=False)
        df = df.sort_values(by=[runDateColumnKey, typeColumnKey, actionColumnKey, aux_debitColumnKey, symbolColumnKey], ascending=False)

        df = df.drop(columns=droppableAuxColumns)
        df = df.replace(replacementHash, regex=True)
        df.loc[(~is_option & ~is_debit), actionColumnKey] = ''
        
        df = df.rename(columns=renamedColumnsHash)
        return df.to_html(classes=styleClasses, index=False)
    

    def is_date(self, value: str):
        try:
            pd.to_datetime(value)
            return True
        except ValueError:
            return False
        
    def is_not_zero(self, value: str):
        try:
            amount = int(value)
            return (amount != 0)
        except ValueError:
            return True
        
    def without_substring(self, value: str):
        if 'JOURNALED'.lower() in str(value).lower():
            return False
        else:
            return True
