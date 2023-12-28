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

        mainColumnKey = 'Run Date'
        df = df.drop(columns=['Exchange Quantity', 'Exchange Currency', 'Exchange Rate', 'Settlement Date'])
        df = df.sort_values(by=mainColumnKey, ascending=False)

        # Apply the custom function to create a Boolean mask
        mask = df[mainColumnKey].apply(self.is_date)
        df = df[mask]

        return df.to_html(classes=styleClasses)
    

    def is_date(self, value: str):
        try:
            pd.to_datetime(value)
            return True
        except ValueError:
            return False
