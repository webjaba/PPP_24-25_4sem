import json
import csv
# from pprint import pprint

# TODO: покрыть тестами


def load_metatable(cfg: dict) -> dict:
    """Функция для загрузки главной таблицы с мета информацией."""
    with open(cfg["tables_info_path"], mode="r", encoding="utf-8") as file:
        jsondata = json.load(file)
        return jsondata


class Table:
    """Класс таблицы."""

    def __init__(self, table_name: str, metatable: dict) -> None:
        """Загрузка общей информации таблицы."""
        self.columns = {}
        self.path = ""
        for table in metatable:
            if table["table"] == table_name:
                cnt = 0
                for column in table["columns"]:
                    self.columns[column["name"]] = {
                        "indx": cnt,
                        "dtype": self.parse_type(column["dtype"])
                    }
                    cnt += 1
                self.path = table["path"]
                break
        if self.path == "":
            print("Table does not exists")

    def select(self, where: str = "", columns: list[str] = ["*"]) -> list:
        """Обработка SELECT запроса."""
        # TODO: дописать обработку условия

        result = []

        with open(self.path, mode="r") as tablefile:
            reader = csv.reader(tablefile)
            reader.__next__()
            for row in reader:

                for col in self.columns:
                    column = self.columns[col]
                    row[column["indx"]] = column["dtype"](row[column["indx"]])

                if where != "":
                    pass

                if columns != ["*"]:
                    new_row = []
                    for col_ in columns:
                        col = self.columns.get(col_, None)
                        if col is not None:
                            new_row.append(row[col["indx"]])
                    row = new_row

                result.append(row)

        return result

    @staticmethod
    def parse_type(dtype: str):
        """Парсинг типа данных."""
        match dtype:
            case "int":
                return int
            case "str":
                return str


print(Table(
    "testtable",
    {
        "tables_info_path": r"tables/tables_info.json"
    }
).select(columns=["*"]))
