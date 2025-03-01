"""Module, that provided api for parsing SQL queries."""


class InvalidQueryError(Exception):
    """Base class for handling exception during parsing SQL queries."""

    def __init__(self, message: str = ""):
        """Initialize error."""
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Strging representation."""
        return f"Invalid query: {self.message}"


class SQLParser:
    """SQL parser class."""

    def __init__(self) -> None:
        """Initialize SQL parser."""
        pass

    def select(self, query: str) -> None:
        """
        Parse SELECT query.

        methods for validating query should have 'validate_' prefix
        """
        query_list = query.split(" ")

        validation_methods = [
            attr
            for attr in dir(self)
            if callable(getattr(self, attr)) and attr[0:9] == "validate_"
        ].__iter__()

        for method in validation_methods:
            if getattr(self, method)(query_list) is False:
                raise InvalidQueryError("Unable to parse query.")

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

    @staticmethod
    def validate_where_condition(query: list[str]) -> bool:
        """Validate WHERE statement."""
        if "WHERE" in query:
            pass
        return True
