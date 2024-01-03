from . import app_constants
from ._shared.managers.baseapp import BaseApp

import pandas as pd
from pandas import DataFrame


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
premiumColumnKey = 'Premium'
dividendColumnKey = 'Dividend'
amountColumnKey = 'Amount'
quantityColumnKey = 'Quantity'

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

sortingPriorityColumns = [runDateColumnKey, 
                          typeColumnKey, 
                          symbolColumnKey, 
                          actionColumnKey, 
                          aux_debitColumnKey,
                          ]

replacementHash = {'YOU SOLD OPENING TRANSACTION' : 'OPENING',
                   'YOU SOLD CLOSING TRANSACTION' : 'CLOSING',
                   'YOU BOUGHT OPENING TRANSACTION' : 'OPENING',
                   'YOU BOUGHT CLOSING TRANSACTION' : 'CLOSING',
                   'YOU BOUGHT' : '',
                   'YOU SOLD' : '',
                   '\\(100 SHS\\)' : '',
                   '\\(Margin\\)' : '',
                   '\\(Cash\\)' : '',
                   }

renamedColumnsHash = {runDateColumnKey : 'Date',
                      symbolColumnKey : 'Ticker',
                      actionColumnKey : 'Note',
                      amountColumnKey : 'Activity',
                      quantityColumnKey : 'Share',
                      }


class QoordiNetAppManager(BaseApp):
    def __init__(self, appName, logFilePath):
        super().__init__(appName, logFilePath)

        from .qoordinet_database import QoordiNetSQLiteManager
        self.databaseManager = QoordiNetSQLiteManager()
        self.databaseManager.prepareEngine(sqlitePath=app_constants.SQLITE_PATH, shouldEcho=self.args.verbose)
        

    def process_data(self, tab_separated):
        rows = tab_separated.strip().split("\n")
        processed_data = [row.split("\t") for row in rows]
        return processed_data
    

    def html_table(self, csv_file, shouldDisplayRaw: bool, styleClass: str):
        df = pd.read_csv(csv_file.file, skiprows=4, header=0)
        
        if shouldDisplayRaw is True:
            return df.to_html(classes=styleClass)
        
        
        df = self.revisedDataFrame(df)
        generated_html = df.to_html(classes=styleClass, index=False)

        return generated_html
    

    def revisedDataFrame(self, df: DataFrame):
        df = df.drop(columns=droppedColumnKeys)

        runDateKeyMask = df[runDateColumnKey].apply(self.is_date)
        actionKeyMask = df[actionColumnKey].apply(self.without_substring)
        amountKeyMask = df[amountColumnKey].apply(self.is_not_zero)
        df = df[runDateKeyMask]
        df = df[actionKeyMask]
        df = df[amountKeyMask]

    
        df[newlyInsertedColumns] = ''
        df = df[rearrangedColumns]

        is_option = df[actionColumnKey].str.contains('CALL|PUT', regex=True, case=False)
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

        is_other_transactions = df[actionColumnKey].str.contains('DEBIT|DEPOSIT|Transfer|CASH CONTRIBUTION', regex=True, case=False)
        df.loc[is_other_transactions, quantityColumnKey] = ''

        is_invested = (df[amountColumnKey] != '') & (df[quantityColumnKey] != '')
        df.loc[is_invested, typeColumnKey] = 'Invested'

        df[aux_debitColumnKey] = is_other_transactions
        df[runDateColumnKey] = pd.to_datetime(df[runDateColumnKey])

        df = df.sort_values(by=sortingPriorityColumns, ascending=False)

        df = df.drop(columns=droppableAuxColumns)
        df = df.replace(replacementHash, regex=True)
        df.loc[(~is_option & ~is_other_transactions), actionColumnKey] = ''
        
        df = df.rename(columns=renamedColumnsHash)

        return df

    

    def is_date(self, value: str):
        try:
            pd.to_datetime(value)
            return True
        except ValueError:
            return False
        
    def is_not_zero(self, value: str):
        try:
            amount = float(value)
            return (amount != 0.0)
        except ValueError:
            return True
        
    def without_substring(self, value: str):
        if 'JOURNALED'.lower() in str(value).lower():
            return False
        else:
            return True
