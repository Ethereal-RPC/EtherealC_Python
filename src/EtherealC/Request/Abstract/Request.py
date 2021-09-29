import sys
from abc import ABC
from types import MethodType

from EtherealC.Core.Model.AbstractType import AbstrackType
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Request.Abstract.RequestConfig import RequestConfig
from EtherealC.Core.Event import Event
from EtherealC.Request.Decorator.Request import RequestAnnotation


def register(instance, net_name, service_name: str, types, config: RequestConfig):
    from EtherealC.Core.Model.TrackException import ExceptionCode, TrackException
    if config is not None:
        instance.config = config
    instance.net_name = net_name
    instance.service_name = service_name
    instance.types = types
    for method_name in dir(instance):
        func = getattr(instance, method_name)
        if isinstance(func.__doc__, RequestAnnotation):
            assert isinstance(func, MethodType)
            annotation: RequestAnnotation = func.__doc__
            if annotation is not None:
                method_id: str = func.__name__

                types = list(func.__annotations__.values())
                if func.__annotations__.get("return") is not None:
                    return_name = func.__annotations__.get('return', None)
                    params = types[:-1:]
                else:
                    raise TrackException(code=ExceptionCode.Core,
                                         message="%s-%s方法中的返回值未定义！".format(net_name, func.__name__))

                if annotation.parameters is None:
                    for param in params:
                        if param is not None:
                            # annotations 有 module 有 class
                            rpc_type: AbstrackType = instance.types.typesByType.get(param, None)
                            if rpc_type is None:
                                raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                                     .format(param.__name__))
                            method_id += "-" + rpc_type.name
                else:
                    for abstract_name in annotation.parameters:
                        if instance.types.typesByName.get(abstract_name, None) is None:
                            raise TrackException(code=ExceptionCode.Core, message="对应的{0}抽象类型对应的实际类型尚未注册"
                                                 .format(abstract_name))
                        method_id += "-" + abstract_name
                invoke = instance.getInvoke(method=func, method_id=method_id, return_name=return_name, annotation=annotation)
                invoke.__annotations__ = func.__annotations__
                invoke.__doc__ = func.__doc__
                invoke.__name__ = func.__name__
                setattr(instance, method_name, invoke)


class Request(ABC):

    def __init__(self):
        self.config = None
        self.service_name = None
        self.net_name = None
        self.exception_event = Event()
        self.log_event = Event()
        self.connectSuccess_event = Event()
        self.client = None
        self.types = None
        self.task = dict()

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