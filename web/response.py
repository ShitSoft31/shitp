from ..base import ShitProtocol
from ..packet import ShitpPacket
from ..mimes import MimeType
from ..status import ShitpStatus


class ShitpWebResponse(ShitProtocol):
    def __init__(self, _status: ShitpStatus, _body: str | bytes | None = None):
        self.__status = _status
        self.__body = _body

    def create(self, _version: str, _mime_type: MimeType) -> ShitpPacket:
        packet = super().create(_version, _mime_type)
        packet.set_header("status", self.__status.value)
        if self.__body is not None:
            packet.set_body(self.__body)

        return packet
