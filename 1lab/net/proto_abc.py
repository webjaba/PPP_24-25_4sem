from abc import ABC, abstractmethod


class AbstractProtocolHandler(ABC):
    MSG_SIZE = 16

    @abstractmethod
    def send(self, conn, msg):
        pass

    @abstractmethod
    def recv(self, conn):
        return ""
