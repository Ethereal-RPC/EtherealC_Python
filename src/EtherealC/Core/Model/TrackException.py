from enum import Enum


class ExceptionCode(Enum):
    Core = 1,
    Runtime = 2


class TrackException(Exception):

    def __init__(self, code: ExceptionCode = None, message=None, exception=None):
        if exception is not None:
            super().__init__(code, "外部库错误")
        super().__init__(code, message)
        self.code = ExceptionCode.Core
        self.message = message
        self.exception = exception
        self.sender = None

