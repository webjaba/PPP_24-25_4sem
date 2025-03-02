"""Module that contains utility staff."""
from typing import TypedDict, Type


class TableDoesNotExistsError(Exception):
    """
    Exception raised when a table does not exist in the database.

    This exception is used to indicate that an
    operation was attempted on a table
    that does not exist in the database. It provides a custom error message.

    Attributes:
        None: This exception does not have additional attributes.

    Methods:
        __str__: Returns a custom error message indicating
            that the table does not exist.

    Example:
        >>> raise TableDoesNotExistsError()
        TableDoesNotExistsError: Table does not exists
    """

    def __init__(self):
        """
        Initialize the TableDoesNotExistsError exception.

        This method calls the parent class's __init__ method
        to set up the exception.
        """
        super().__init__()

    def __str__(self):
        """
        Return a custom error message.

        Returns:
            str: A string indicating that the table does not exist.
        """
        return "Table does not exists"


class Column(TypedDict):
    """Class for information about column."""

    indx: int
    dtype: Type
