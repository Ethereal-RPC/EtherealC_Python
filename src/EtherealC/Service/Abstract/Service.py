from abc import ABC, abstractmethod
from types import MethodType

from EtherealC.Core.Model.AbstractType import AbstrackType
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Service.Abstract import ServiceConfig
from EtherealC.Core import Event
from EtherealC.Service.Decorator.Service import ServiceAnnotation


def register(instance, net_name, service_name, config: ServiceConfig):
    instance.config = config
    instance.net_name = net_name
    instance.service_name = service_name
    for method_name in dir(instance):
        func = getattr(instance, method_name)
        if isinstance(func.__doc__, ServiceAnnotation):
            assert isinstance(func, MethodType)
            method_id = func.__name__
            if func.__doc__.paramters is None:

                if func.__annotations__.get("return") is not None:
                    params = list(func.__annotations__.values())[:-1:]
                else:
                    params = list(func.__annotations__.values())
                for param in params:
                    rpc_type: AbstrackType = instance.config.types.typesByType.get(param, None)
                    if rpc_type is not None:
                        method_id = method_id + "-" + rpc_type.name
                    else:
                        raise TrackException(code=ExceptionCode.Core, message="{name}方法中的{param}类型参数尚未注册"
                                             .format(name=func.__name__, param=param.__name__))
            else:
                for param in func.__doc__.paramters:
                    rpc_type: AbstrackType = instance.config.types.abstractType.get(type(param), None)
                    if rpc_type is not None:
                        method_id = method_id + "-" + rpc_type.name
                    else:
                        raise TrackException(code=ExceptionCode.Core,
                                             message="%s方法中的%s抽象类型参数尚未注册".format(func.__name__, param))
            if instance.methods.get(method_id, None) is not None:
                raise TrackException(code=ExceptionCode.Core,
                                     message="服务方法{name}已存在，无法重复注册！".format(name=method_id))
            instance.methods[method_id] = func


class Service(ABC):
    def __init__(self):
        self.config: ServiceConfig = None
        self.methods = dict()
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
