from . import app_constants
from ._shared.managers.baseapp import BaseApp

import pandas as pd
from pandas import DataFrame, Timestamp

import json


droppedColumnKeys = ['Exchange Quantity',
                     'Exchange Currency', 
                     'Exchange Rate',
                     'Settlement Date',
                     'Currency',
                     'Accrued Interest',
                     'Price',
                     'Commission',
                     'Fees',
                     ]

droppedColumnKeys_olderBefore20240307 = ['Security Description',
                                         'Security Type',
                                        ]

droppedColumnKeys_newerSince20240307 = ['Description',
                                        'Type',
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
                   'BUY CANCEL CLOSING TRANSACTION' : 'CLOSING',
                   'YOU BOUGHT' : '',
                   'YOU SOLD' : '',
                   '\\(100 SHS\\)' : '',
                   '\\(Margin\\)' : '',
                   '\\(Cash\\)' : '',
                   }

dateColumnKey = 'Date'

renamedColumnsHash = {runDateColumnKey : dateColumnKey,
                      symbolColumnKey : 'Ticker',
                      actionColumnKey : 'Note',
                      amountColumnKey : 'Activity',
                      quantityColumnKey : 'Share',
                      }

table_name = 'qoordinetActivities'

class QoordiNetAppManager(BaseApp):
    loadedDf: DataFrame
    last_activity: Timestamp


    def __init__(self, appName, logFilePath):
        super().__init__(appName, logFilePath)

        from .qoordinet_database import QoordiNetSQLiteManager
        self.databaseManager = QoordiNetSQLiteManager()
        self.databaseManager.prepareEngine(sqlitePath=app_constants.SQLITE_PATH, shouldEcho=self.args.verbose)

        self.loadedDf = DataFrame()


    def __appConfiguration(self):
        configurationData = None
        try:
            with open(app_constants.APP_CONFIGURATION, 'r') as file:
                configurationData = json.load(file)
        except FileNotFoundError:
            self.logger.info(f"File not found: {app_constants.APP_CONFIGURATION}")
        finally:
            pass

        self.logger.info(f"configurationData: {configurationData}")    
        return configurationData


    def __reloadDataFrame(self):
        self.loadedDf = pd.read_sql_table(table_name, self.databaseManager.engine)
        self.loadedDf.fillna('', inplace=True)
        
        self.last_activity = pd.to_datetime(self.loadedDf.loc[self.loadedDf.index[-1]][dateColumnKey])

        self.logger.info(f"self.loadedDf: {self.loadedDf}")
        self.logger.info(f"last_activity: {self.last_activity}")


    def activities_list(self):
        self.__reloadDataFrame()

        generated_list = self.loadedDf.to_dict(orient='records')
        return generated_list
    

    def delete_last(self, days: int | None = None):
        selected_days = max((days or 0), 1)
        self.logger.info(f"selected_days: {selected_days}")

        if self.loadedDf.empty:
            self.__reloadDataFrame()

        selected_date = self.loadedDf.loc[self.loadedDf.index[-1]][dateColumnKey]
        filteredDf = self.loadedDf[self.loadedDf[dateColumnKey] != selected_date]

        filteredDf.to_sql(table_name, con=self.databaseManager.engine, if_exists='replace', index=False)
        

    def html_table(self, csv_file, shouldDisplayRaw: bool, styleClass: str):
        if shouldDisplayRaw is True:
            df = pd.read_csv(csv_file.file, header=0)
            return df.to_html(classes=styleClass)
        
        df = pd.read_csv(csv_file.file, skiprows=2, header=0)
        df = self.revisedDataFrame(df)
        df.fillna('', inplace=True)
        generated_html = df.to_html(classes=styleClass, index=False)

        return generated_html

    
    def save_into_database(self, csv_file, styleClass: str):
        df = pd.read_csv(csv_file.file, skiprows=2, header=0)
        df = self.revisedDataFrame(df)

        df.to_sql(table_name, con=self.databaseManager.engine, if_exists='append', index=False)
    
    def build_database(self, csv_file, styleClass: str):
        df = pd.read_csv(csv_file.file, header=0)
        runDateKeyMask = df[dateColumnKey].apply(self.is_date)
        df = df[runDateKeyMask]

        df.to_sql(table_name, con=self.databaseManager.engine, if_exists='replace', index=False)


    def revisedDataFrame(self, df: DataFrame):
        columnDroppedDF = df
        columnDroppedDF = columnDroppedDF.drop(columns=droppedColumnKeys)
        try:
            columnDroppedDF = columnDroppedDF.drop(columns=droppedColumnKeys_olderBefore20240307)
        except KeyError:
            try:
                columnDroppedDF = columnDroppedDF.drop(columns=droppedColumnKeys_newerSince20240307)
            except KeyError:
                pass

        df = columnDroppedDF
        

        runDateKeyMask = df[runDateColumnKey].apply(self.is_date)
        actionKeyMask = df[actionColumnKey].apply(self.without_substring)
        amountKeyMask = df[amountColumnKey].apply(self.is_not_zero)
        quantityKeyMask = df[quantityColumnKey].apply(self.is_not_zero)

        df = df[runDateKeyMask]
        df = df[actionKeyMask]
        df = df[amountKeyMask | quantityKeyMask]

    
        df[typeColumnKey] = ''
        df[premiumColumnKey] = None
        df[dividendColumnKey] = None
        df = df[rearrangedColumns]


        is_option = df[actionColumnKey].str.contains('CALL|PUT|CALLS|PUTS', regex=True, case=False)
        df.loc[is_option, typeColumnKey] = 'OPTION'
        
        is_option_not_assigned = is_option & ~(df[actionColumnKey].str.contains('ASSIGNED', regex=True, case=False))
        df.loc[is_option_not_assigned, premiumColumnKey] = df.loc[is_option_not_assigned, amountColumnKey]
        df.loc[is_option_not_assigned, amountColumnKey] = None
        df.loc[is_option_not_assigned, quantityColumnKey] = None
        
        df[aux_tickerColumnKey] = df[symbolColumnKey].str.extract(r'-([A-Z]+)').fillna('').astype(str)
        df.loc[is_option_not_assigned, symbolColumnKey] = df.loc[is_option_not_assigned, aux_tickerColumnKey]
            
    
        is_dividend = (df[actionColumnKey].str.contains('DIVIDEND', case=False)) & (df[quantityColumnKey] == 0)
        df.loc[is_dividend, typeColumnKey] = 'dividend'
        df.loc[is_dividend, dividendColumnKey] = df.loc[is_dividend, amountColumnKey]
        df.loc[is_dividend, amountColumnKey] = None
        df.loc[is_dividend, quantityColumnKey] = None

        is_passive = (df[actionColumnKey].str.contains('INTEREST EARNED', regex=True, case=False))
        df.loc[is_passive, typeColumnKey] = 'passive'
        df.loc[is_passive, symbolColumnKey] = 'interest'
        df.loc[is_passive, quantityColumnKey] = df.loc[is_passive, amountColumnKey]
        df.loc[is_passive, amountColumnKey] = None

        is_other_transactions = df[actionColumnKey].str.contains('DEBIT|DEPOSIT|Transfer|CASH CONTRIBUTION|FEE', regex=True, case=False)
        df.loc[is_other_transactions, quantityColumnKey] = None

        is_invested = ~is_option & (df[amountColumnKey].isna() == False) & (df[quantityColumnKey].isna() == False)
        df.loc[is_invested, typeColumnKey] = 'Invested'

        df[aux_debitColumnKey] = is_other_transactions


        try:
            df[runDateColumnKey] = pd.to_datetime(df[runDateColumnKey].str.strip()).dt.strftime('%m/%d/%Y')
        except ValueError:
            try:
                df[runDateColumnKey] = pd.to_datetime(df[runDateColumnKey].str.strip(), format='%b-%d-%Y').dt.strftime('%m/%d/%Y')
            except ValueError:
                self.logger.info(f"to_datetime, reformatting failed")
                pass
            
            pass

        df[runDateColumnKey] = pd.to_datetime(df[runDateColumnKey])

        df[accountColumnKey] = df[accountColumnKey].str.strip()
        df[typeColumnKey] = df[typeColumnKey].str.strip()
        df[symbolColumnKey] = df[symbolColumnKey].str.strip()
        df[actionColumnKey] = df[actionColumnKey].str.strip()


        df = df.sort_values(by=sortingPriorityColumns, ascending=True)

        df = df.drop(columns=droppableAuxColumns)
        
        df = df.replace(replacementHash, regex=True)
        configurationData = self.__appConfiguration()
        if configurationData != None:
            df = df.replace(configurationData['replacementHash'], regex=False)
                        
        df.loc[(~is_option & ~is_other_transactions), actionColumnKey] = ''
        

        current_latest = df.loc[df.index[-1]][runDateColumnKey]
        numberOfDays = (current_latest - self.last_activity).days
        numberOfDays = max(min(numberOfDays, 30), 0)
        self.logger.info(f"current_latest: {current_latest}")
        self.logger.info(f"last_activity: {self.last_activity}")
        self.logger.info(f"numberOfDays: {numberOfDays}")

        latest_dates = df[runDateColumnKey].drop_duplicates().nlargest(numberOfDays)
        selected_rows = df[df[runDateColumnKey].isin(latest_dates)]
        df = selected_rows
        
        revisedDataFrame = df.rename(columns=renamedColumnsHash)

        return revisedDataFrame

    

    def is_date(self, value: str):
        try:
            pd.to_datetime(value)
            return True
        
        except ValueError:
            try:
                pd.to_datetime(value, format='%b-%d-%Y')
                return True
            
            except ValueError:
                self.logger.info(f"is_date: {False} : {value}")
                return False

        
    def is_not_zero(self, value: str):
        try:
            return (float(value) != 0.0)
        except ValueError:
            return True
        
    def without_substring(self, value: str):
        if 'JOURNALED'.lower() in str(value).lower():
            return False
        else:
            return True
