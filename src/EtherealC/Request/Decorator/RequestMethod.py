from enum import Enum

from EtherealC.Request.Decorator import InvokeTypeFlags


class RequestMethod:
    def __init__(self):
        self.timeout = None
        self.invokeType = InvokeTypeFlags.Remote | InvokeTypeFlags.ReturnRemote

    def __call__(self, func):
        func.__doc__ = self
        return func