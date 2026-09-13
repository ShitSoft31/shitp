import struct

from .status import ShitpStatus
from .methods import ShitpMethod
from .mimes import MimeType


"""
SHITP — Super Hybrid Information Transfer Protocol

Base serialization and parsing utilities for the SHITP protocol.

Packet structure:

    +------------------+------------------+------------------+-------------+
    |  Header Size     |   Body Size      |     Headers      |    Body     |
    |    4 bytes       |    4 bytes       |   variable       |  variable   |
    +------------------+------------------+------------------+-------------+

The header and body sizes are encoded as unsigned 32-bit integers
in network byte order (big-endian).

Header format:

    version=0.1.0
    method=FETCH
    mime_type=text/markdown
    host=example.com
    custom_header=value

Each header is represented as a UTF-8 encoded `name=value` pair
terminated by a newline character.
"""


def create_header(**kwargs) -> str:
    header_str = '\n'.join(f"{k}={v}" for k, v in kwargs.items())
    return header_str + '\n'

def create_client_request(
    version: str,
    method: ShitpMethod,
    mime_type: MimeType,
    host: str,
    body: str | bytes = "",
    headers: dict | None = None
):
    """
    Serialize a client request into the SHITP wire format.

    :param version: SHITP protocol version.
    :param method: HTTP-like method represented by a :class:`ShitpMethod`.
    :param mime_type: MIME type of the request body.
    :param host: Target SHITP host.
    :param body: Request payload as a string or raw bytes.
    :param headers: Additional SHITP headers.

    :return: Serialized SHITP request as bytes.
    """

    headers = {} if headers is None else headers

    header_str = create_header(
        version=version,
        method=method.value,
        mime_type=mime_type.value,
        host=host,
        **headers
    )

    raw_header = header_str.encode("utf-8")

    if isinstance(body, str):
        raw_body = body.encode("utf-8")
    else:
        raw_body = body

    header_size = len(raw_header)
    body_size = len(raw_body)

    # Encode both sizes as unsigned 32-bit integers in network byte order.
    pack = struct.pack("!II", header_size, body_size)

    return pack + raw_header + raw_body


def create_server_response(
    version: str,
    status: ShitpStatus,
    mime_type: MimeType,
    message: str,
    body: str | bytes = "",
    headers: dict | None = None
):
    """
    Serialize a server response into the SHITP wire format.

    :param version: SHITP protocol version.
    :param status: Response status represented by a :class:`ShitpStatus`.
    :param mime_type: MIME type of the response body.
    :param message: Human-readable response message.
    :param body: Response payload as a string or raw bytes.
    :param headers: Additional SHITP headers.

    :return: Serialized SHITP response as bytes.
    """

    headers = {} if headers is None else headers

    header_str = create_header(
        version=version,
        status=status.value,
        mime_type=mime_type.value,
        message=message,
        **headers
    )

    raw_header = header_str.encode("utf-8")

    if isinstance(body, str):
        raw_body = body.encode("utf-8")
    else:
        raw_body = body

    header_size = len(raw_header)
    body_size = len(raw_body)

    # Encode both sizes as unsigned 32-bit integers in network byte order.
    pack = struct.pack("!II", header_size, body_size)

    return pack + raw_header + raw_body


def parse_shitp_request(
    header_size: int,
    body_size: int,
    raw_request: bytes
):
    """
    Parse a serialized SHITP request.

    The first 8 bytes containing the header and body sizes must be
    removed before passing the packet to this function.

    :param header_size: Size of the encoded header in bytes.
    :param body_size: Size of the encoded body in bytes.
    :param raw_request: Raw request data excluding the 8-byte size prefix.

    :return:
        A tuple containing:

        - ``dict``: Parsed SHITP headers.
        - ``bytes``: Raw request body.
    """
    raw_header = raw_request[:header_size]
    raw_body = raw_request[header_size:header_size + body_size]

    header = raw_header.decode("utf-8")

    header_dict = {}

    for header_line in header.splitlines():
        name, value = header_line.split("=", 1)
        header_dict[name] = value

    return header_dict, raw_body
