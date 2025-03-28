from net.proto_abc import AbstractProtocolHandler
import socket


class ProtocolHandler(AbstractProtocolHandler):
    def __init__(self):
        pass

    def send(self, conn: socket.socket, msg: bytes):
        for i in range(len(msg) // self.MSG_SIZE):
            if i * self.MSG_SIZE >= len(msg):
                conn.send(msg[i * self.MSG_SIZE::])
            conn.send(msg[i * self.MSG_SIZE:(i + 1) * self.MSG_SIZE])

    def recv(self, conn: socket.socket):
        request = bytes()
        while True:
            data = conn.recv(self.MSG_SIZE)
            if len(data) == 0:
                break
            request = b''.join(
                (request, data)
            )
        return request
