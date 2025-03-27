from .utils import Column
from sql.utils import Query
from typing import Type
import json
import csv
import os
import sys
import re

# TODO: покрыть тестами


def load_metatable(cfg: dict) -> dict[str, dict]:
    """
    Load table with meta inforamation.

    Arguments:
        cfg (dict): config object

    Returns:
        dict: table object
    """
    path = cfg.get("metatable_path", "")

    if path == "":
        print("metatable path must be specified")
        sys.exit(1)

    if not os.path.exists(path):
        print(f"metatable does not exists, path: {path}")
        sys.exit(1)

    with open(path, mode="r", encoding="utf-8") as file:
        jsondata = json.load(file)
        return jsondata


class Table:
    """Table class."""

    def __init__(
            self,
            table_name: str,
            metatable: dict[str, dict]
    ) -> None:
        """
        Initialize table.

        Arguments:
            table_name (str): name of a table, that would be used in a query
            metatable (dict): metatable, that would be used to parse
                information about table
        """
        self.columns: dict[str, Column] = dict()
        self.path = ""
        cnt = 0
        table = metatable[table_name]
        for column in table["columns"]:
            self.columns[column["name"]] = {
                "indx": cnt,
                "dtype": self.parse_type(column["dtype"])
            }
            cnt += 1
        self.path = table["path"]
        if self.path == "":
            print("Table does not exists")

    def process_condition(self, condition: str) -> str:
        column_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b(?=\s*[=<>!]|\s+AND|\s+OR|$)')
        columns = set(column_pattern.findall(condition))
        missing = [col for col in columns if col not in self.columns]

        if missing:
            raise ValueError(
                f"Column mapping missing for: {', '.join(missing)}"
            )

        def replacer(match):
            col = match.group(0)
            return f"row[{self.columns[col]['indx']}]"

        result = column_pattern.sub(replacer, condition)

        return result

    def select(self, query: Query) -> list:
        """
        Handle SELECT query.

        Arguments:
            query (Query): validated SELECT query.

        Returns:
            list: a list of rows
        """

        result = []

        with open(self.path, mode="r") as tablefile:
            reader = csv.reader(tablefile)
            reader.__next__()
            for row in reader:

                for col in self.columns:
                    column = self.columns[col]
                    row[column["indx"]] = column["dtype"](row[column["indx"]])

                if query["condition"] != "":
                    cond = self.process_condition(query['condition'])

                    if not eval(cond):
                        continue

                if query["columns"] != ["*"]:
                    new_row = []
                    for col_name in query["columns"]:
                        col_obj = self.columns.get(col_name, None)
                        if col_obj is not None:
                            new_row.append(row[col_obj["indx"]])
                    row = new_row

                result.append(row)

        return result

    @staticmethod
    def parse_type(dtype: str) -> Type:
        """
        Parse dtype and returns corresponding type.

        Arguments:
            dtype (str): data type in str format

        Returns:
            type: a type of data
        """
        match dtype:
            case "int":
                return int
            case "str":
                return str
            case _:
                return str
