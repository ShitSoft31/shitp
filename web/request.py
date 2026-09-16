from ..base import ShitProtocol
from ..packet import ShitpPacket
from ..mimes import MimeType
from ..methods import ShitpMethod


class ShitpWebRequest(ShitProtocol):
    def __init__(
        self,
        _method: ShitpMethod,
        _host: str,
        _body: str | bytes | None = None,
    ):
        self.__method = _method
        self.__host = _host
        self.__body = _body

    def create(self, _version: str, _mime_type: MimeType) -> ShitpPacket:
        packet = super().create(_version, _mime_type)
        packet.set_header("method", self.__method.value)
        packet.set_header("host", self.__host)
        if self.__body is not None:
            packet.set_body(self.__body)

        return packet
