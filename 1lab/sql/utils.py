from typing import TypedDict, List


class Query(TypedDict):
    table: str
    columns: List[str]
    condition: str


class InvalidQueryError(Exception):
    """Base class for handling exception during parsing SQL queries."""

    def __init__(self, message: str = ""):
        """Initialize error."""
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Strging representation."""
        if self.message == "":
            return "Invalid query"
        return f"Invalid query: {self.message}"
