from enum import Enum


class LogCode(Enum):
    Core = 1
    Runtime = 2


class TrackLog:
    def __init__(self, code, message):
        self.code: LogCode = code
        self.message: str = message
        self.sender = None