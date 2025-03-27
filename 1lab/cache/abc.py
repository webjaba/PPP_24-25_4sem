from abc import ABC, abstractmethod


class AbstractCache(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_query_existance(self, query: str) -> bool:
        return False

    @abstractmethod
    def get_query(self, query: str) -> bytes:
        return bytes()

    @abstractmethod
    def add_query(self, query: str, result: bytes) -> None:
        pass
