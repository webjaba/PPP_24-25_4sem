import struct

class Deserializer:
    def __init__(self):
        self.byteorder_int = '>q'
        self.byteorder_float = '>d'
        self.encoding = 'utf-8'

    def deserialize(self, data: bytes):
        """Главный метод десериализации"""
        if not data:
            raise ValueError("Empty data")

        type_byte = data[0:1]
        content = data[1:]

        if type_byte == b'i':
            return self.deserialize_int(content)
        elif type_byte == b'f':
            return self.deserialize_float(content)
        elif type_byte == b's':
            return self.deserialize_str(content)
        elif type_byte == b'l':
            return self.deserialize_list(content)
        elif type_byte == b'd':
            return self.deserialize_dict(content)
        else:
            raise ValueError(f"Unknown type byte: {type_byte}")

    def deserialize_list(self, data: bytes) -> list:
        """Десериализация списка с рекурсивной обработкой элементов"""
        length = struct.unpack(self.byteorder_int, data[:8])[0]
        offset = 8
        result = []

        for _ in range(length):
            elem_type = data[offset:offset+1]
            elem_data = data[offset+1:]

            elem, elem_size = self._deserialize_element(elem_type, elem_data)
            result.append(elem)
            offset += 1 + elem_size

        return result

    def deserialize_dict(self, data: bytes) -> dict:
        """Десериализация словаря с рекурсивной обработкой пар ключ-значение"""
        length = struct.unpack(self.byteorder_int, data[:8])[0]
        offset = 8
        result = {}

        for _ in range(length):
            key_type = data[offset:offset+1]
            key_data = data[offset+1:]
            key, key_size = self._deserialize_element(key_type, key_data)
            offset += 1 + key_size

            val_type = data[offset:offset+1]
            val_data = data[offset+1:]
            value, val_size = self._deserialize_element(val_type, val_data)
            offset += 1 + val_size

            result[key] = value

        return result

    def _deserialize_element(self, elem_type: bytes, data: bytes) -> tuple[object, int]:
        """Вспомогательный метод для десериализации элемента"""
        if elem_type == b'i':
            return struct.unpack(self.byteorder_int, data[:8])[0], 8
        elif elem_type == b'f':
            return struct.unpack(self.byteorder_float, data[:8])[0], 8
        elif elem_type == b's':
            str_len = struct.unpack('>I', data[:4])[0]
            return data[4:4+str_len].decode(self.encoding), 4 + str_len
        elif elem_type == b'l':
            # Для списка сначала получаем его длину
            length = struct.unpack(self.byteorder_int, data[:8])[0]
            offset = 8
            items = []

            for _ in range(length):
                sub_type = data[offset:offset+1]
                item, item_size = self._deserialize_element(sub_type, data[offset+1:])
                items.append(item)
                offset += 1 + item_size

            return items, offset
        elif elem_type == b'd':
            # Для словаря аналогично
            length = struct.unpack(self.byteorder_int, data[:8])[0]
            offset = 8
            result = {}

            for _ in range(length):
                # Ключ
                key_type = data[offset:offset+1]
                key, key_size = self._deserialize_element(key_type, data[offset+1:])
                offset += 1 + key_size

                val_type = data[offset:offset+1]
                value, val_size = self._deserialize_element(val_type, data[offset+1:])
                offset += 1 + val_size

                result[key] = value

            return result, offset
        else:
            raise ValueError(f"Unknown element type: {elem_type}")

    def deserialize_int(self, data: bytes) -> int:
        return struct.unpack(self.byteorder_int, data[:8])[0]

    def deserialize_float(self, data: bytes) -> float:
        return struct.unpack(self.byteorder_float, data[:8])[0]

    def deserialize_str(self, data: bytes) -> str:
        str_len = struct.unpack('>I', data[:4])[0]
        return data[4:4+str_len].decode(self.encoding)