from rich.table import Table
from rich import box


class TableFactory:
    def __init__(self, title: str, columns: list):
        # init the table
        self.table = Table(title=title, header_style='bold magenta', box=box.ROUNDED)
        self.rows = 0

        # add the columns
        for col in columns:
            self.table.add_column(col, justify='center', vertical='middle')

    def insert(self, data: list):
        """Insert the data in the table"""
        self.table.add_row(*data)
        self.rows += 1
