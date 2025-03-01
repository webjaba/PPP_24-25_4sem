from table_manager import TableManager
import json
import os


def test_returning_metatable():
    meta = {
        "test": {
            "columns": [
                {"name": "id", "dtype": "int"},
                {"name": "col1", "dtype": "str"},
                {"name": "col2", "dtype": "str"}
            ],
            "path": "teststorage/test.csv"
        },
        "test2": {
            "columns": [
                {"name": "id", "dtype": "int"},
                {"name": "col1", "dtype": "str"},
                {"name": "col2", "dtype": "str"}
            ],
            "path": "teststorage/test2.csv"
        }
    }
