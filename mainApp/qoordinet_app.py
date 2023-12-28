from ._shared.managers.baseapp import BaseApp


class QoordiNetAppManager(BaseApp):
    def process_data(self, tab_separated):
        rows = tab_separated.strip().split("\n")
        processed_data = [row.split("\t") for row in rows]
        return processed_data
    