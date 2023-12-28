from ._shared.managers.baseapp import BaseApp

import pandas as pd


class QoordiNetAppManager(BaseApp):
    def process_data(self, tab_separated):
        rows = tab_separated.strip().split("\n")
        processed_data = [row.split("\t") for row in rows]
        return processed_data
    

    def html_table(self, csv_file, styleClasses: str):
        df = pd.read_csv(csv_file.file, skiprows=4, header=0)
        self.logger.info(df.columns)

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
        df = df.drop(columns=droppedColumnKeys)

        mainColumnKey = 'Run Date'
        actionColumnKey = 'Action'
        amountColumnKey = 'Amount'
        
        rearrangedColumns = [mainColumnKey, 'Account', 'Type', 'Symbol', actionColumnKey, 'Premium', 'Dividend', amountColumnKey, 'Quantity']
        df['Type'] = ''
        df['Premium'] = ''
        df['Dividend'] = ''
        df = df[rearrangedColumns]

        mainKeyMask = df[mainColumnKey].apply(self.is_date)
        actionKeyMask = df[actionColumnKey].apply(self.without_substring)
        amountKeyMask = df[amountColumnKey].apply(self.is_not_zero)

        df = df[mainKeyMask]
        df = df[actionKeyMask]
        df = df[amountKeyMask]

        df = df.replace(
            {'YOU SOLD OPENING TRANSACTION' : 'OPENING',
             'YOU SOLD CLOSING TRANSACTION' : 'CLOSING',
             'YOU BOUGHT OPENING TRANSACTION' : 'OPENING',
             'YOU BOUGHT CLOSING TRANSACTION' : 'CLOSING',
             'YOU BOUGHT' : '',
             'YOU SOLD' : '',
             '\(100 SHS\)' : '',
             '\(Margin\)' : '',
             '\(Cash\)' : '',
             }, regex=True)
        

        df = df.sort_values(by=[mainColumnKey, actionColumnKey], ascending=False)

        return df.to_html(classes=styleClasses)
    

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
