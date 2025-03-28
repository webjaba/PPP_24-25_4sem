"""."""
from cache.abc import AbstractCache


class InMemoryCache(AbstractCache):
    """."""

    def __init__(self) -> None:
        """."""
        self.storage: dict[str, bytes] = dict()

    def get_query_existance(self, query: str) -> bool:
        """."""
        if self.storage.get(query, None):
            return True
        return False

    def get_query(self, query: str) -> bytes:
        """."""
        if self.get_query_existance(query):
            return self.storage[query]
        return bytes()

    def add_query(self, query: str, result: bytes) -> None:
        """."""
        if self.get_query_existance(query):
            return None
        self.storage[query] = result
