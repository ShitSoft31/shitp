# SHITP — Super Hybrid Information Transfer Protocol

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![Version](https://img.shields.io/badge/version-0.1.2-orange)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

> **Simple structure. Known sizes. Easy parsing.**
> A lightweight data transfer protocol designed from the ground up.

## What is SHITP?

SHITP (Super Hybrid Information Transfer Protocol) is a lightweight, general-purpose data transfer protocol designed from the ground up. Its goal is to carry data in a format that is predictable in structure, fast to parse, and easy to implement.

Unlike application-specific protocols, SHITP does not impose a particular communication model. It provides a simple packet structure that can be used as the foundation for different applications, services, and communication systems.

This repository contains the core building blocks of the protocol:

- **Packet serialization and parsing** (`packet.py`)
- Protocol-related enums for methods, MIME types, and status codes

The transport layer (TCP sockets) and application-level implementations are intentionally kept outside the core protocol.

## What makes it different?

SHITP builds on the experience of established protocols but defines its own rules. Its key design decisions:

- **Known packet sizes.** The first 8 bytes of every packet contain the header and body sizes explicitly. A parser knows exactly how much data it needs to read without scanning for delimiters or guessing where the payload ends.
- **Simple header structure.** Every header is a single-line `name=value` pair. No escape sequences, no continuation lines, no multi-stage parsing rules.
- **Deterministic packets.** The same input always produces the same output. Packet parsing does not depend on external application state.
- **Native binary support.** A body given as `str` is encoded as UTF-8; given as `bytes`, it is carried as-is.
- **Transport-independent design.** SHITP defines how packets are structured, not how they are transmitted. TCP sockets, servers, and client implementations belong to separate layers.

## Project layout

```text
shitp/
├── packet.py    # ShitpPacket — headers, body, encoding and decoding
├── methods.py   # ShitpMethod enum
├── mimes.py     # MimeType enum
└── status.py    # ShitpStatus enum
```

## Wire format

Every SHITP packet consists of four parts:

```text
+------------------+------------------+------------------+-------------+
|  Header Size     |   Body Size      |     Headers      |    Body     |
|    4 bytes       |    4 bytes       |   variable       |  variable   |
+------------------+------------------+------------------+-------------+
```

- **Header Size** and **Body Size** are unsigned 32-bit integers encoded in network byte order (big-endian).
- **Headers** consist of the `name=value` pairs described below.
- **Body** contains the actual payload.

The first 8 bytes form the packet's length prefix:

1. Read the first 8 bytes.
2. Decode the header and body sizes.
3. Read the remaining bytes according to the decoded sizes.
4. Parse the headers and body.

This allows the receiving application to process packets incrementally without assuming that the entire packet arrives in a single read operation.

## Header format

Every header is a single-line `name=value` pair, UTF-8 encoded and terminated by `\n`:

```text
version=0.1.2
method=FETCH
mime_type=shitp/markdown
host=example.com
custom_header=value
```

The first `=` character separates the name from the value; values may contain additional `=` characters.

Headers are stored as part of the packet. `set_header()` allows you to add or replace individual headers without requiring application-specific builders.

## Installation

The package is not published on PyPI yet. Clone the repository and add the `shitp/` directory to your project — there are no external dependencies.

Requirements:

- Python 3.10+ (type hints use the `str | bytes` syntax)
- Standard library only (`struct`, `enum`)

## Usage

### Building a packet

```python
from shitp.packet import ShitpPacket

packet = ShitpPacket()

packet.set_header("version", "0.1.2")
packet.set_header("method", "FETCH")
packet.set_header("mime_type", "shitp/markdown")
packet.set_header("host", "example.com")

packet.set_body("# Hello, SHITP!")

raw_packet = packet.encode()
```

### Adding custom headers

```python
packet.set_header("user_agent", "shitp-client/0.1.2")
packet.set_header("authorization", "Bearer token")

raw_packet = packet.encode()
```

### Working with binary data

SHITP supports both text and binary payloads:

```python
packet.set_body("Hello, SHITP!")
text_packet = packet.encode()

packet.set_body(b"\x00\x01\x02\x03")
binary_packet = packet.encode()
```

String payloads are automatically encoded using UTF-8, while byte payloads are preserved as-is.

### Decoding a packet

The receiving application is responsible for reading the 8-byte length prefix and collecting the complete packet before passing it to the decoder.

```python
from shitp.packet import ShitpPacket

packet = ShitpPacket.decode(raw_packet)

print(packet.get_header("method"))  # 'FETCH'
print(packet.get_header("host"))    # 'example.com'
print(packet.get_body())            # b'# Hello, SHITP!'
```

## What's in v0.1.2?

### Methods — `shitp.methods`

| Method | Description |
|---|---|
| `FETCH` | Retrieves a resource from the server |
| `PUSH` | Sends a resource to the server |

### MIME types — `shitp.mimes`

| MIME type | Description |
|---|---|
| `shitp/markdown` | Markdown content (the only type so far) |

### Statuses — `shitp.status`

| Status | Description |
|---|---|
| `OK` | Request succeeded |
| `NOT_FOUND` | Resource not found |
| `INTERNAL_SERVER_ERROR` | Server-side error |
| `TIMEOUT` | Timeout |
| `RESPONSE_ERROR` | Response error |

### Classes — `shitp.packet`

| Member | Purpose |
|---|---|
| `ShitpPacket.set_header(name, value)` | Adds or replaces a header |
| `ShitpPacket.get_header(name)` | Returns a header value, or `None` if absent |
| `ShitpPacket.set_body(str \| bytes)` | Sets the packet body (`str` is UTF-8 encoded) |
| `ShitpPacket.get_body()` | Returns the raw body bytes |
| `ShitpPacket.encode()` | Serializes the packet into wire bytes |
| `ShitpPacket.decode(raw_packet)` | Parses wire bytes into a packet |

## Roadmap

- [x] Separate protocol responsibilities and redesign SHITP for general-purpose use.
- [x] Refactor for object-oriented programming.
- [x] Separate packet serialization from transport and application-level logic.
- [ ] More methods, MIME types, and status codes.
- [ ] Typed data structures for headers.
- [ ] Official protocol specification document.

The transport layer (TCP sockets) and server frameworks built on top of SHITP are out of scope for this repository. They will live in separate repositories.

## Contributing

PRs and issues are always welcome. For larger changes, open an issue to discuss first; for small fixes, feel free to send a PR directly.
