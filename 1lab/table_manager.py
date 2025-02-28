from table import load_metatable


class TableManager:
    """Table manager class."""

    def __init__(self, cfg: dict) -> None:
        """Initialize manager."""
        self.metatable: dict = load_metatable(cfg)
        self.tables: list = []
