# SHITP — Super Hybrid Information Transfer Protocol

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![Version](https://img.shields.io/badge/version-0.1.0-orange)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

> **Simple structure. Known sizes. Easy parsing.**
> A lightweight data transfer protocol designed from the ground up.

## What is SHITP?

SHITP (Super Hybrid Information Transfer Protocol) is a lightweight data
transfer protocol designed from the ground up. Its goal is to carry data in a
format that is predictable in structure, fast to parse, and easy to implement.

This repository contains the core building blocks of the protocol:

- Helper functions for **packet serialization and parsing** (`base.py`)
- The protocol's `method`, `mime`, and `status` enums

## What makes it different?

SHITP builds on the experience of established text-based protocols, but sets
its own rules. The standout design decisions:

- **Sizes are always known.** The first 8 bytes of every packet carry the
  header and body sizes explicitly. A parser never has to scan for or guess
  where the payload ends — read the first 8 bytes and you know the entire
  packet.
- **Simple header structure.** Every header is a single-line `name=value`
  pair. No escape sequences, no continuation lines, no multi-stage parsing
  rules.
- **Deterministic packets.** The same input always produces the same output;
  a parser holds no state.
- **Native binary support.** A body given as `str` is encoded as UTF-8;
  given as `bytes`, it is carried as-is.

## Project layout

```
shitp/
├── base.py      # Packet serialization and parsing
├── methods.py   # ShitpMethod enum
├── mimes.py     # MimeType enum
└── status.py    # ShitpStatus enum
```

## Wire format

Every SHITP packet consists of four parts:

```
+------------------+------------------+------------------+-------------+
|  Header Size     |   Body Size      |     Headers      |    Body     |
|    4 bytes       |    4 bytes       |   variable       |  variable   |
+------------------+------------------+------------------+-------------+
```

- **Header Size** and **Body Size** are unsigned 32-bit integers encoded in
  network byte order (big-endian).
- **Headers** consist of the `name=value` pairs described below.
- **Body** is the payload of the request or response.

## Header format

Every header is a single-line `name=value` pair, UTF-8 encoded and terminated
by `\n`:

```
version=0.1.0
method=FETCH
mime_type=shitp/markdown
host=example.com
custom_header=value
```

The first `=` character separates the name from the value; values may contain
additional `=` characters. Standard headers are added automatically by the
protocol; the `headers` parameter lets you add as many custom headers as you
like.

## Installation

The package is not published on PyPI yet. Clone the repository and add the
`shitp/` directory to your project — there are no external dependencies.

Requirements:

- Python 3.10+ (type hints use the `str | bytes` syntax)
- Standard library only (`struct`, `enum`)

## Usage

Creating a client request and a server response:

```python
from shitp.base import create_client_request, create_server_response
from shitp.methods import ShitpMethod
from shitp.mimes import MimeType
from shitp.status import ShitpStatus

request = create_client_request(
    version="0.1.0",
    method=ShitpMethod.FETCH,
    mime_type=MimeType.MARKDOWN,
    host="example.com",
    body="# Hello, SHITP!",
    headers={"user_agent": "shitp-client/0.1.0"},
)

response = create_server_response(
    version="0.1.0",
    status=ShitpStatus.OK,
    mime_type=MimeType.MARKDOWN,
    message="Request processed successfully.",
    body="# Hello!",
)
```

Parsing a packet (you strip the 8-byte size prefix yourself):

```python
import struct

from shitp.base import parse_shitp_request

header_size, body_size = struct.unpack("!II", request[:8])
headers, body = parse_shitp_request(header_size, body_size, request[8:])

print(headers)  # {'version': '0.1.0', 'method': 'FETCH', ...}
print(body)     # b'# Hello, SHITP!'
```

## What's in v0.1.0?

### Methods — `shitp.methods`

| Method  | Description                            |
|---------|----------------------------------------|
| `FETCH` | Retrieves a resource from the server   |
| `PUSH`  | Sends a resource to the server         |

### MIME types — `shitp.mimes`

| MIME type        | Description                       |
|------------------|-----------------------------------|
| `shitp/markdown` | Markdown content (the only type so far) |

### Statuses — `shitp.status`

| Status                  | Description       |
|-------------------------|-------------------|
| `OK`                    | Request succeeded |
| `NOT_FOUND`             | Resource not found|
| `INTERNAL_SERVER_ERROR` | Server-side error |
| `TIMEOUT`               | Timeout           |
| `RESPONSE_ERROR`        | Response error    |

### Functions — `shitp.base`

| Function                   | Purpose                                              |
|----------------------------|------------------------------------------------------|
| `create_header(**kwargs)`  | Builds a header string                               |
| `create_client_request()`  | Serializes a client request into the wire format     |
| `create_server_response()` | Serializes a server response into the wire format    |
| `parse_shitp_request()`    | Parses a packet, returning `(headers, body)`         |

## Roadmap

- [x] Responsibilities should be separated. The protocol should be redesigned for general-purpose use.
- [x] Refactor for object-oriented programming
- [ ] More methods, MIME types, and status codes
- [ ] Typed data structures for headers
- [ ] Official protocol specification document

The transport layer (TCP sockets) and the server frameworks built on top of
it are out of scope for this repository; they will live in separate repos.

## Contributing

PRs and issues are always welcome. For larger changes, open an issue to
discuss first; for small fixes, feel free to send a PR directly.
