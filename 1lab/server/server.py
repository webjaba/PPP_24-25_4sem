"""."""
from sql.utils import Query
from net.proto_abc import AbstractProtocolHandler
from net.proto import ProtocolHandler
from cache.cache import get_cache_obj
from serialization.deserializer import Deserializer
from abc import ABC, abstractmethod
import socket
import sys
import logging


class Parser(ABC):
    """."""

    @abstractmethod
    def select(self, query: str):
        """."""
        return Query(table="", columns=[], condition="")


class Manager(ABC):
    """."""

    @abstractmethod
    def handle_query(self, query: Query) -> bytes:
        """."""
        return bytes()


class Server:
    """."""

    def __init__(
            self,
            cfg: dict,
            sqlparser: Parser,
            tablemanager: Manager,
            protocol_handler: AbstractProtocolHandler = ProtocolHandler(),
    ):
        """."""
        self.logger = logging.getLogger('Server')
        self.ip = cfg.get('ip')
        self.port = cfg.get('port')
        self.protocol = protocol_handler
        self.sqlparser = sqlparser
        self.tablemanager = tablemanager
        self.deserializer = Deserializer()
        self.cache = get_cache_obj(cfg=cfg)
        if self.port is None or self.ip is None:
            self.logger.info(msg='ip and port must be specified in config')
            sys.exit(1)

    def handle_client(self, conn):
        """."""
        serialized_data = bytes()
        try:
            msg = self.protocol.recv(conn)
            msg = self.deserializer.deserialize_str(
                msg
            )
            self.logger.info(msg=f'message recieved, len = {len(msg)}')
        except:
            exc_type, exc_value, _ = sys.exc_info()
            self.logger.error(
                msg=f'error during recieving a message: {exc_type.__name__}')

        try:
            if self.cache.get_query_existance(msg):
                self.logger.info(msg='getting response from cache')
                self.protocol.send(conn, self.cache.get_query(msg))
        except:
            exc_type, exc_value, _ = sys.exc_info()
            self.logger.error(
                msg=f'error of getting response from cache: {exc_type.__name__}')

        try:
            serialized_data = self.tablemanager.handle_query(
                self.sqlparser.select(msg)
            )
            self.logger.info(
                msg=f'request proccessed successfully, response len = {len(serialized_data)}'
            )
        except:
            exc_type, exc_value, _ = sys.exc_info()
            self.logger.error(
                msg=f'error of processing request: {exc_type.__name__}')

        try:
            self.cache.add_query(query=msg, result=serialized_data)
            self.logger.info(msg='response was cached successfuly')
        except:
            exc_type, exc_value, _ = sys.exc_info()
            self.logger.error(
                msg=f'error during caching: {exc_type.__name__}: {exc_value}')
        self.protocol.send(conn, serialized_data)
        self.logger.info(msg=f'msg was sended: {len(serialized_data)}')

    def run(self):
        """."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.ip, self.port))
            self.logger.info(f'started on {(self.ip, self.port)}')
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    self.logger.info(f'connect {addr}')
                    self.handle_client(conn)
