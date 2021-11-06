import sys
from abc import ABC, abstractmethod
from EtherealC.Core.Model.AbstractTypes import AbstractTypes
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Core.Event import Event
from EtherealC.Request.Decorator.Request import Request


def register(instance):
    from EtherealC.Request.Decorator.RequestMethod import RequestMethod
    for method_name in dir(instance):
        func = getattr(instance, method_name)
        if isinstance(func.__doc__, RequestMethod):
            annotation: RequestMethod = func.__doc__
            if annotation is not None:
                invoke = instance.getInvoke(func=func, annotation=annotation)
                invoke.__annotations__ = func.__annotations__
                invoke.__doc__ = func.__doc__
                invoke.__name__ = func.__name__
                setattr(instance, method_name, invoke)


@Request()
class Request(ABC):

    def __init__(self):
        self.config = None
        self.name = None
        self.net = None
        self.exception_event = Event()
        self.log_event = Event()
        self.connectSuccess_event = Event()
        self.task = dict()
        self.types = AbstractTypes()

    def OnLog(self, log: TrackLog = None, code=None, message=None):
        if log is None:
            log = TrackLog(code=code, message=message)
        log.server = self
        self.log_event.onEvent(log=log)

    def OnException(self, exception: TrackException = None, code=None, message=None):
        if exception is None:
            exception = TrackException(code=code, message=message)
        exception.server = self
        self.exception_event.onEvent(exception=exception)

    def OnConnectSuccess(self, **kwargs):
        self.connectSuccess_event.onEvent(request=self)

    @abstractmethod
    def Initialize(self):
        pass

    @abstractmethod
    def UnInitialize(self):
        pass
