"""main файл."""
from internal.config import read_cfg
from tables.table_manager import TableManager
from sql.sql_parser import SQLParser
from server.server import Server


def main():
    """."""
    cfg = read_cfg()

    sql_parser = SQLParser()

    table_manager = TableManager(cfg)

    server = Server(
        protocol_handler=None,
        cfg=cfg,
        sqlparser=sql_parser,
        tablemanager=table_manager,
        logger=None
    )

    server.run()


if __name__ == "__main__":
    main()
