import socket
import sys
from abc import ABC, abstractmethod


class ProtocolHandler(ABC):
    MSG_SIZE = 16

    @abstractmethod
    def send(self, conn, msg):
        pass

    @abstractmethod
    def recv(self, conn):
        pass


class Parser(ABC):

    @abstractmethod
    def select(self, query: str):
        pass


class Server:
    def __init__(
            self,
            protocol_handler: ProtocolHandler,
            cfg: dict,
            sqlparser: Parser,
            tablemanager,
            logger=None
    ):
        self.ip = cfg.get('ip')
        self.port = cfg.get('port')
        self.protocol = protocol_handler
        self.logger = logger
        self.sqlparser = sqlparser
        self.tablemanager = tablemanager
        if self.port is None or self.ip is None:
            print('ip and port must be specified in config')
            sys.exit(1)

    def handle_client(self, conn):
        pass

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.ip, self.port))
            if self.logger:
                self.logger.info(f'started on {(self.host, self.port)}')
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    if self.logger:
                        self.logger.info(f'connect {addr}')
                    self.handle_client(conn)

                if self.logger:
                    self.logger.info(f'closed on {(self.host, self.port)}')
