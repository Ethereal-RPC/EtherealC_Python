from abc import ABC, abstractmethod
from types import MethodType

from EtherealC.Core.Model.AbstractType import AbstrackType
from EtherealC.Core.Model.AbstractTypes import AbstractTypes
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Service.Abstract import ServiceConfig
from EtherealC.Core import Event
from EtherealC.Service.Decorator.Service import Service


def register(service):
    for method_name in dir(service):
        func = getattr(service, method_name)
        from EtherealC.Service.Decorator.ServiceMethod import ServiceMethod
        if isinstance(func.__doc__, ServiceMethod):
            method_id = func.__name__
            if func.__annotations__.get("return") is not None:
                parameterInfos = list(func.__annotations__.values())[:-1:]
            else:
                parameterInfos = list(func.__annotations__.values())
            for parameterInfo in parameterInfos:
                abstractType: AbstrackType = service.types.typesByType.get(parameterInfo, None)
                if abstractType is None:
                    raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                         .format(parameterInfo))
                method_id += "-" + abstractType.name
            if service.methods.get(method_id, None) is not None:
                raise TrackException(code=ExceptionCode.Core,
                                     message="服务方法{name}已存在，无法重复注册！".format(name=method_id))
            service.methods[method_id] = func


@Service()
class Service(ABC):
    def __init__(self):
        self.config: ServiceConfig = None
        self.methods = dict()
        self.net_name = None
        self.name = None
        self.exception_event: Event = Event.Event()
        self.log_event: Event = Event.Event()
        self.interceptorEvent = list()
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

    def OnInterceptor(self, net, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(net, self, method, token):
                return False
        return True

    @abstractmethod
    def Initialize(self):
        pass

    @abstractmethod
    def UnInitialize(self):
        pass
