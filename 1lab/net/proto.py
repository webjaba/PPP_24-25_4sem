"""."""
from net.proto_abc import AbstractProtocolHandler
import socket


class ProtocolHandler(AbstractProtocolHandler):
    """."""

    def __init__(self):
        """."""
        super().__init__()

    def send(self, conn: socket.socket, msg: bytes):
        """."""
        total_length = len(msg)
        conn.sendall(total_length.to_bytes(8, byteorder='big'))

        for i in range(0, total_length, self.MSG_SIZE):
            chunk = msg[i:i + self.MSG_SIZE]
            conn.sendall(chunk)

    def recv(self, conn: socket.socket) -> bytes:
        """."""
        length_data = conn.recv(8)
        if not length_data:
            return b''

        total_length = int.from_bytes(length_data, byteorder='big')

        received_data = bytearray()
        while len(received_data) < total_length:
            chunk = conn.recv(min(
                self.MSG_SIZE, total_length - len(received_data)
            ))
            if not chunk:
                raise ConnectionError("Connection broken while receiving data")
            received_data.extend(chunk)

        return bytes(received_data)
