class NoneCache:
    def __init__(self):
        pass

    def get_query_existance(self, query) -> bool:
        return False

    def get_query(self, query) -> list:
        return []

    def add_query(self, query, result) -> None:
        pass