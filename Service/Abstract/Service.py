from abc import ABC, abstractmethod
from types import MethodType

from Core.Model.AbstractType import AbstrackType
from Core.Model.TrackException import TrackException, ExceptionCode
from Core.Model.TrackLog import TrackLog
from Service.Abstract import ServiceConfig
from Core import Event
from Service.Decorator.Service import ServiceAnnotation


class Service(ABC):
    def __init__(self):
        self.config: ServiceConfig = None
        self.methods = dict()
        self.instance = None
        self.net_name = None
        self.service_name = None
        self.exception_event: Event = Event.Event()
        self.log_event: Event = Event.Event()
        self.interceptorEvent = list()

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

    def OnInterceptor(self, net, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(net, self, method, token):
                return False
        return True

    @abstractmethod
    def register(self, net_name, service_name, instance, config: ServiceConfig):
        pass
