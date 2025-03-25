from abc import ABC, abstractmethod


class AbstractCache(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_query_existance(self, query: str) -> bool:
        return False

    @abstractmethod
    def get_query(self, query: str) -> list:
        return []

    @abstractmethod
    def add_query(self, query: str, result: list) -> None:
        pass
