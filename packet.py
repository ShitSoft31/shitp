import struct


class ShitpPacket:
    def __init__(self):
        self.__headers = {}
        self.__body = b""

    def encode(self) -> bytes:
        header = "\n".join(f"{k}={v}" for k, v in self.__headers.items())
        raw_header = header.encode("utf-8")

        raw_header_len = len(raw_header)
        raw_body_len = len(self.__body)

        size_pack = struct.pack("!II", raw_header_len, raw_body_len)

        return size_pack + raw_header + self.__body

    def set_header(self, name: str, value: str):
        self.__headers[name] = value

    def set_body(self, body: str | bytes):
        if isinstance(body, str):
            self.__body = body.encode("utf-8")
        else:
            self.__body = body

    def get_header(self, name: str) -> str | None:
        return self.__headers.get(name)

    def get_body(self) -> bytes | str:
        return self.__body
