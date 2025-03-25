from .table import load_metatable, Table
from sql.utils import Query
from .utils import TableDoesNotExistsError
from abc import ABC, abstractmethod
from cache.cache import get_cache_obj


class AbstractSerializer(ABC):

    @abstractmethod
    def serialize_list(self, msg: list) -> bytes:
        return bytes()

    @abstractmethod
    def serialize_dict(self, msg: dict) -> bytes:
        return bytes()


class TableManager:
    """Table manager class."""

    def __init__(self, cfg: dict, serializer: AbstractSerializer) -> None:
        """Initialize manager."""
        self.metatable: dict[str, dict] = load_metatable(cfg)
        self.tables: dict[str, Table] = dict()
        self.meta_for_user: dict[str, list[dict[str, str]]] = dict()
        self.serializer = serializer
        for table in self.metatable:
            self.meta_for_user.update(
                {table: self.metatable[table]["columns"]}
            )
        self.serialized_meta_for_user = self.serializer.serialize_dict(
            self.meta_for_user
        )

    def handle_query(
        self, query: Query
    ) -> bytes:
        # Union[list, dict[str, list[dict[str, str]]]]
        """
        Handle query.

        Arguments:
            query (Query): validated query that needs to be handled

        Returns:
            list or dict: if table is 'meta' returns dict,
                otherwise returns list
        """
        if query["table"] == "meta":
            return self.serialized_meta_for_user

        if self.metatable.get(query["table"], None) is None:
            raise TableDoesNotExistsError()

        table = self.tables.get(query["table"], None)
        if table is None:
            table = Table(table_name=query["table"], metatable=self.metatable)

        result = table.select(query)

        return self.serializer.serialize_list(result)
