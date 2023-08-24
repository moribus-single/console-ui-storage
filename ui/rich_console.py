from typing import Any

from rich.table import Table
from rich.console import Console
from rich.pretty import pprint


class UIConsole:
    def __init__(self):
        self.console = Console()

    def log(self, data: str):
        """Logging in the console"""
        self.console.print(data)

    def print(self, table: Table):
        """Printing the table in the console"""
        self.console.print(table)

    def pprint(self, obj: Any):
        """Pretty print any object"""
        pprint(obj)
