from .table import load_metatable, Table
from sql.utils import Query
from .utils import TableDoesNotExistsError
from typing import Union


class TableManager:
    """Table manager class."""

    def __init__(self, cfg: dict) -> None:
        """Initialize manager."""
        self.metatable: dict[str, dict] = load_metatable(cfg)
        self.tables: dict[str, Table] = dict()
        self.meta_for_user: dict[str, list[dict[str, str]]] = dict()
        for table in self.metatable:
            self.meta_for_user.update(
                {table: self.metatable[table]["columns"]}
            )

    def handle_query(
        self, query: Query
    ) -> Union[list, dict[str, list[dict[str, str]]]]:
        """
        Handle query.

        Arguments:
            query (Query): validated query that needs to be handled

        Returns:
            list or dict: if table is 'meta' returns dict,
                otherwise returns list
        """
        if query["table"] == "meta":
            return self.meta_for_user

        if self.metatable.get(query["table"], None) is None:
            raise TableDoesNotExistsError()

        table = self.tables.get(query["table"], None)
        if table is None:
            table = Table(table_name=query["table"], metatable=self.metatable)

        result = table.select(query)

        return result
