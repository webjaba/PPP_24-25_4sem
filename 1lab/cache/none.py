from cache.abc import AbstractCache


class NoneCache(AbstractCache):
    def __init__(self):
        pass

    def get_query_existance(self, query: str) -> bool:
        return False

    def get_query(self, query: str) -> bytes:
        return bytes()

    def add_query(self, query: str, result: bytes) -> None:
        pass
