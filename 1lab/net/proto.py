from net.proto_abc import AbstractProtocolHandler
import socket


# class ProtocolHandler(AbstractProtocolHandler):
#     def __init__(self):
#         pass

#     def send(self, conn: socket.socket, msg: bytes):
#         for i in range(len(msg) // self.MSG_SIZE):
#             if i * self.MSG_SIZE >= len(msg):
#                 conn.send(msg[i * self.MSG_SIZE::])
#             conn.send(msg[i * self.MSG_SIZE:(i + 1) * self.MSG_SIZE])

#     def recv(self, conn: socket.socket):
#         request = bytes()
#         while True:
#             data = conn.recv(self.MSG_SIZE)
#             if len(data) == 0:
#                 break
#             request = b''.join(
#                 (request, data)
#             )
#         return request


class ProtocolHandler(AbstractProtocolHandler):
    def __init__(self):
        super().__init__()

    def send(self, conn: socket.socket, msg: bytes):
        """
        Отправляет сообщение по частям указанного размера.
        Сначала отправляет длину сообщения (8 байт), затем само сообщение.
        """
        # Отправляем длину сообщения (8 байт, big-endian)
        total_length = len(msg)
        conn.sendall(total_length.to_bytes(8, byteorder='big'))
        
        # Отправляем само сообщение по частям
        for i in range(0, total_length, self.MSG_SIZE):
            chunk = msg[i:i + self.MSG_SIZE]
            conn.sendall(chunk)

    def recv(self, conn: socket.socket) -> bytes:
        """
        Получает сообщение, сначала читая его длину,
        затем получая данные пока не получит все ожидаемые байты.
        """
        # Получаем длину сообщения (первые 8 байт)
        length_data = conn.recv(8)
        if not length_data:
            return b''
        
        total_length = int.from_bytes(length_data, byteorder='big')
        
        # Получаем само сообщение
        received_data = bytearray()
        while len(received_data) < total_length:
            chunk = conn.recv(min(self.MSG_SIZE, total_length - len(received_data)))
            if not chunk:
                raise ConnectionError("Connection broken while receiving data")
            received_data.extend(chunk)
        
        return bytes(received_data)