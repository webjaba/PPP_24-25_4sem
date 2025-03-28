"""main файл."""
from internal.config import read_cfg
from tables.table_manager import TableManager
from internal.logger import set_up_logger
from sql.sql_parser import SQLParser
from server.server import Server
from serialization.serializer import Serializer


def main():
    """."""
    cfg = read_cfg()

    set_up_logger()

    serializer = Serializer()

    sql_parser = SQLParser()

    table_manager = TableManager(cfg, serializer=serializer)

    print('starting server...')
    server = Server(
        cfg=cfg,
        sqlparser=sql_parser,
        tablemanager=table_manager
    )

    server.run()


if __name__ == "__main__":
    main()
