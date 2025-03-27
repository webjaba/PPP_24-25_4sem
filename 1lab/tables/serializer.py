import struct


class Serializer:
    def __init__(self):
        self.byteorder_int = '>q'
        self.byteorder_float = '>d'
        self.encoding = 'utf-8'

    def serialize_list(self, data: list) -> bytes:

        serialized_data: list[bytes] = [self.serialize_int(len(data))]

        for elem in data:

            serialized_elem = bytes()
            serialized_type = bytes()

            if type(elem) is int:
                serialized_elem = self.serialize_int(elem)
                serialized_type = self.serialize_str('i')
            elif type(elem) is float:
                serialized_elem = self.serialize_float(elem)
                serialized_type = self.serialize_str('f')
            elif type(elem) is str:
                serialized_elem = self.serialize_str(elem)
                serialized_type = self.serialize_str('s')
            else:
                raise TypeError()

            serialized_data.extend(
                (serialized_type, serialized_elem)
            )

        return b''.join(serialized_data)

    def serialize_arg(self, arg) -> tuple[bytes, bytes]:

        serialized_elem = bytes()
        serialized_type = bytes()

        if type(arg) is int:
            serialized_elem = self.serialize_int(arg)
            serialized_type = self.serialize_str('i')
        elif type(arg) is float:
            serialized_elem = self.serialize_float(arg)
            serialized_type = self.serialize_str('f')
        elif type(arg) is str:
            serialized_elem = self.serialize_str(arg)
            serialized_type = self.serialize_str('s')
        elif type(arg) is list:
            serialized_elem = self.serialize_list(arg)
            serialized_type = self.serialize_str('l')
        elif type(arg) is dict:
            serialized_elem = self.serialize_dict(arg)
            serialized_type = self.serialize_str('d')
        else:
            raise TypeError()

        return serialized_type, serialized_elem

    def serialize_dict(self, data: dict) -> bytes:

        serialized_dict: list[bytes] = [
            self.serialize_str('d'),
            self.serialize_int(len(data)),
        ]

        for key in data:
            serialized_dict.extend((
                *self.serialize_arg(key),
                *self.serialize_arg(data[key])
            ))

        return b''.join(serialized_dict)

    def serialize_str(self, text: str):
        encoded_text = text.encode(self.encoding)
        return struct.pack(
            f'I{len(encoded_text)}s', len(encoded_text), encoded_text
        )

    def serialize_int(self, num: int) -> bytes:
        return struct.pack(self.byteorder_int, num)

    def serialize_float(self, num: float) -> bytes:
        return struct.pack(self.byteorder_float, num)
