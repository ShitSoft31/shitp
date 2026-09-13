from enum import Enum

class ShitpStatus(Enum):
    OK = 'OK'
    NOT_FOUND = 'NOT_FOUND'
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    TIMEOUT = 'TIMEOUT'
    RESPONSE_ERROR = 'RESPONSE_ERROR'
