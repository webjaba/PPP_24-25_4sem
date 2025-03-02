import json
import os
from sql.utils import Query
from tables.table_manager import TableManager


def test_returning_metatable() -> None:

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

    res = {
        "test": [
                {"name": "id", "dtype": "int"},
                {"name": "col1", "dtype": "str"},
                {"name": "col2", "dtype": "str"}
        ],
        "test2": [
                {"name": "id", "dtype": "int"},
                {"name": "col1", "dtype": "str"},
                {"name": "col2", "dtype": "str"}
        ]
    }

    query: Query = {
        "table": "meta",
        "columns": ["table", "columns",],
        "condition": ""
    }

    with open("testmeta.json", "w", encoding="utf-8") as file:
        json.dump(meta, file, ensure_ascii=False, indent=4)

    manager = TableManager(cfg={"metatable_path": "testmeta.json"})
    actual = manager.handle_query(query)
    os.remove("testmeta.json")
    assert actual == res
