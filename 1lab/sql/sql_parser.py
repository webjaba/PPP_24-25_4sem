"""Module, that provided api for parsing SQL queries."""
from .utils import Query, InvalidQueryError


class SQLParser:
    """SQL parser class."""

    def __init__(self) -> None:
        """Initialize SQL parser."""
        self.possible_operators = (
            "<", ">", "<=", ">=", "<>", "=", "AND", "OR", "NOT"
        )

    def select(self, query: str) -> Query:
        """
        Parse SELECT query.

        methods for validating query should have 'validate_' prefix
        """
        result: Query = {
            "table": "",
            "columns": [],
            "condition": "",
        }

        if query == "INFO":
            result["table"] = "meta"
            result["columns"].extend(["table", "columns"])
            return result

        query_list = query.split(" ")

        validation_methods = [
            attr
            for attr in dir(self)
            if callable(getattr(self, attr)) and attr[0:9] == "validate_"
        ].__iter__()

        for method in validation_methods:
            if getattr(self, method)(query_list) is False:
                raise InvalidQueryError("Unable to parse query.")

        keyword = "SELECT"

        for i in range(1, len(query)):
            part = query[i]
            match keyword:
                case "SELECT":
                    if part == "FROM":
                        keyword = part
                        continue
                    else:
                        if part[-1] == ",":
                            result["columns"].append(part[:-1])
                case "FROM":
                    if part == "WHERE":
                        keyword = part
                        continue
                    else:
                        if part[-1] == ";":
                            result["table"] = part[:-1]
                            break
                        else:
                            result["table"] = part
                case "WHERE":
                    if result["condition"] == "":
                        result["condition"] = part
                    else:
                        if part[-1] == ";":
                            part = part[:-1]
                        result["condition"] = " ".join(
                            (result["condition"], part)
                        )

        return result

    @staticmethod
    def validate_struct(query: list[str]) -> bool:
        """Check the SELECT and FROM phrases."""
        if "SELECT" not in query or "FROM" not in query:
            return False
        from_indx = query.index("FROM")
        if query.index("SELECT") > from_indx:
            return False
        if query.count("SELECT") != 1 or query.count("FROM") != 1:
            return False
        if "WHERE" in query:
            if query.count("WHERE") != 1:
                return False
            if query.index("WHERE") < from_indx:
                return False

        return True

    @staticmethod
    def validate_columns_and_table(query: list[str]) -> bool:
        """Validate writed columns names and table name."""
        cols_cnt = 0
        for i in range(1, len(query)):
            elem = query[i]
            match elem:
                case "FROM":
                    if i + 1 == len(query):  # this solution for validating
                        return False         # table name may be not scalable
                    if cols_cnt == 0:
                        return False
                    break
                case _:
                    if query[i+1] != "FROM" and elem[-1] != ",":
                        return False
                    if query[i+1] == "FROM" and elem[-1] == ",":
                        return False
                    cols_cnt += 1
        return True

    def validate_where_condition(self, query: list[str]) -> bool:
        """Validate WHERE statement."""
        if "WHERE" in query:

            condition = ""

            condition_list = query[query.index("WHERE") + 1:len(query)]

            for i in range(len(condition_list)):
                if condition == "":
                    condition = condition_list[i]
                else:
                    condition = " ".join((condition, condition_list[i]))

            stack = []

            for char in condition:
                match char:
                    case "(":
                        stack.append(char)
                    case ")":
                        if len(stack) == 0:
                            return False
                        stack.pop(-1)
                    case _:
                        continue

        # TODO: дописать валидацию правильной последовательности аргументов
        return True
