from enum import Enum


class ErrorCode(Enum):
    Intercepted = 1,
    NotFoundService = 2,
    NotFoundMethod = 3,
    NotFoundNet = 4,
    BufferFlow = 5,
    Common = 6,
    MaxConnects = 7


class Error:
    def __init__(self, **kwargs):
        self.Code = None
        self.Message = None
        self.Data = None
