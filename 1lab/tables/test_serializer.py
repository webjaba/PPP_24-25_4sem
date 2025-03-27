import struct


class Serializer:
    def __init__(self):
        self.byteorder_int = '>q'
        self.byteorder_float = '>d'
        self.encoding = 'utf-8'

    def serialize(self, data) -> bytes:
        """Рекурсивная сериализация любого поддерживаемого типа"""
        if isinstance(data, int):
            return self.serialize_int(data)
        elif isinstance(data, float):
            return self.serialize_float(data)
        elif isinstance(data, str):
            return self.serialize_str(data)
        elif isinstance(data, list):
            return self.serialize_list(data)
        elif isinstance(data, dict):
            return self.serialize_dict(data)
        else:
            raise TypeError(f"Unsupported type: {type(data)}")

    def serialize_list(self, data: list) -> bytes:
        """Сериализация списка с рекурсивной обработкой элементов"""
        serialized_items = [self.serialize(item) for item in data]
        return b'l' + struct.pack(self.byteorder_int, len(data)) + b''.join(serialized_items)

    def serialize_dict(self, data: dict) -> bytes:
        """Сериализация словаря с рекурсивной обработкой ключей и значений"""
        serialized_items = []
        for key, value in data.items():
            if not isinstance(key, (str, int, float)):
                raise TypeError("Dictionary keys must be str, int or float")
            serialized_items.append(self.serialize(key))
            serialized_items.append(self.serialize(value))
        return b'd' + struct.pack(self.byteorder_int, len(data)) + b''.join(serialized_items)

    def serialize_int(self, num: int) -> bytes:
        return b'i' + struct.pack(self.byteorder_int, num)

    def serialize_float(self, num: float) -> bytes:
        return b'f' + struct.pack(self.byteorder_float, num)

    def serialize_str(self, text: str) -> bytes:
        encoded = text.encode(self.encoding)
        return b's' + struct.pack('>I', len(encoded)) + encoded
