import struct

from .mimes import MimeType
from .packet import ShitpPacket


class ShitProtocol:
    def __init__(self):
        pass

    def create(self, _version: str, _mime_type: MimeType) -> ShitpPacket:
        packet = ShitpPacket()
        packet.set_header("version", _version)
        packet.set_header("mime_type", _mime_type.value)
        return packet

    def decode(self, _raw_packet: bytes) -> ShitpPacket:
        packet = ShitpPacket()

        header_size, body_size = struct.unpack("!II", _raw_packet[:8])
        raw_header = _raw_packet[8 : 8 + header_size].decode("utf-8")
        raw_body = _raw_packet[8 + header_size : 8 + header_size + body_size]

        for header_line in raw_header.splitlines():
            name, value = header_line.split("=", 1)
            packet.set_header(name, value)

        packet.set_body(raw_body)

        return packet
