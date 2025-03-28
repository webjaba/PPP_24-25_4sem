from sql.utils import Query
from net.proto_abc import AbstractProtocolHandler
from net.proto import ProtocolHandler
from cache.cache import get_cache_obj
from abc import ABC, abstractmethod
import socket
import sys
import logging


class Parser(ABC):

    @abstractmethod
    def select(self, query: str):
        return Query(table="", columns=[], condition="")


class Manager(ABC):

    @abstractmethod
    def handle_query(self, query: Query) -> bytes:
        return bytes()


class Server:
    def __init__(
            self,
            cfg: dict,
            sqlparser: Parser,
            tablemanager: Manager,
            protocol_handler: AbstractProtocolHandler = ProtocolHandler(),
    ):
        self.logger = logging.getLogger('Server')
        self.ip = cfg.get('ip')
        self.port = cfg.get('port')
        self.protocol = protocol_handler
        self.sqlparser = sqlparser
        self.tablemanager = tablemanager
        self.cache = get_cache_obj(cfg=cfg)
        if self.port is None or self.ip is None:
            self.logger.info(msg='ip and port must be specified in config')
            sys.exit(1)

    def handle_client(self, conn):
        try:
            msg = self.protocol.recv(conn)
            self.logger.info(msg=f'message recieved, len = {len(msg)}')
        except Exception() as err:
            self.logger.error(msg=f'error during recieving a message: {err}')

        try:
            if self.cache.get_query_existance(msg):
                self.logger.info(msg='getting response from cache')
                return self.cache.get_query(msg)
        except Exception() as err:
            self.logger.error(
                msg=f'error of getting response from cache: {err}'
            )

        try:
            serialized_data = self.tablemanager.handle_query(
                self.sqlparser.select(msg)
            )
            self.logger.info(
                msg=f'request proccessed successfully, response len = {len(serialized_data)}'
            )
        except Exception() as err:
            self.logger.error(
                msg=f'error of processing request: {err}'
            )

        try:
            self.cache.add_query(query=msg, result=serialized_data)
            self.logger.info(msg='response was cached successfuly')
        except Exception as err:
            self.logger.error(msg=f'error during caching: {err}')

        self.protocol.send(serialized_data)

    def run(self):
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

                if self.logger:
                    self.logger.info(f'closed on {(self.host, self.port)}')
