class TableDoesNotExistsError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Table does not exists"
