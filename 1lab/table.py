import json
import csv
# from pprint import pprint


class Table:
    """Класс таблицы."""

    def __init__(self, table_name: str, cfg: dict) -> None:
        """Загрузка общей информации таблицы."""
        self.columns = {}
        self.path = ""
        with open(cfg["tables_info_path"], mode="r", encoding="utf-8") as file:
            jsondata = json.load(file)
            for table in jsondata:
                if table["table"] == table_name:
                    cnt = 0
                    for column in table["columns"]:
                        self.columns[column["name"]] = {
                            "indx": cnt,
                            "type": self.parse_type(column["dtype"])
                        }
                        cnt += 1
                    self.path = table["path"]
                    break
        if self.path == "":
            print("Table does not exists")

    def select(self, where: str = "") -> list:
        """Обработка SELECT запроса."""
        # TODO: дописать обработку условия
        # TODO: дописать конвертацию типа данных

        result = []

        with open(self.path, mode="r") as tablefile:
            reader = csv.reader(tablefile)
            reader.__next__()
            for row in reader:
                if where != "":
                    pass
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
