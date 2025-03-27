"""Module that contains utility staff."""
from typing import TypedDict, Type


class TableDoesNotExistsError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Table does not exists"


class Column(TypedDict):
    """Class for information about column."""

    indx: int
    dtype: Type
