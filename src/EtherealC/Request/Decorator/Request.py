from enum import Enum

from EtherealC.Request.Decorator import InvokeTypeFlags


def Request(parameters=None, timeout=None, invokeType=None):
    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)

        annotation = RequestAnnotation()
        annotation.parameters = parameters
        annotation.timeout = timeout
        if invokeType is not None:
            annotation.invokeType = invokeType
        Func.__doc__ = annotation
        Func.__name__ = func.__name__
        Func.__annotations__ = func.__annotations__
        return Func

    return getFunc


class RequestAnnotation:
    def __init__(self):
        self.parameters = None
        self.timeout = None
        self.invokeType = InvokeTypeFlags.Remote | InvokeTypeFlags.ReturnRemote
