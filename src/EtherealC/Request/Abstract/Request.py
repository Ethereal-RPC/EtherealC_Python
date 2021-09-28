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


def register(instance, net_name, service_name: str, config: RequestConfig):
    from EtherealC.Core.Model.TrackException import ExceptionCode, TrackException
    instance.net_name = net_name
    instance.service_name = service_name
    instance.config = config
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

                if annotation.paramters is None:
                    for param in params:
                        if param is not None:
                            # annotations 有 module 有 class
                            rpc_type: AbstrackType = instance.config.types.typesByType.get(param, None)
                            if rpc_type is None:
                                raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                                     .format(param.__name__))
                            method_id += "-" + rpc_type.name
                else:
                    for abstract_name in annotation.paramters:
                        if instance.config.types.typesByName.get(abstract_name, None) is None:
                            raise TrackException(code=ExceptionCode.Core, message="对应的{0}抽象类型对应的实际类型尚未注册"
                                                 .format(abstract_name))
                        method_id += "-" + abstract_name
                invoke = instance.getInvoke(method_id=method_id, return_name=return_name, annotation=annotation)
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

    def getInvoke(self, method_id, return_name, annotation):
        def invoke(*args, **kwargs):
            parameters = list()
            parameters.append(None)
            for arg in args:
                abstract_type: AbstrackType = self.config.types.typesByType.get(type(arg), None)
                if abstract_type is None:
                    raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                         .format(arg.__name__))
                parameters.append(abstract_type.serialize(arg))

            request = ClientRequestModel(method_id=method_id, params=parameters, service=self.service_name)
            if return_name is None:
                self.client.SendClientRequestModel(request)
            else:
                request.Id = str(self.random.randint(0, sys.maxsize))
                while self.task.get(request.Id) is not None:
                    request.Id = str(self.random.randint(0, sys.maxsize))
                self.task[request.Id] = request
                try:
                    timeout = annotation.timeout
                    if timeout is not None:
                        timeout = self.config.timeout
                    if self.client.SendClientRequestModel(request):
                        response: ClientResponseModel = request.Get(timeout)
                        if response is not None:
                            if response.Error is not None:
                                raise TrackException(code=ExceptionCode.Runtime,
                                                     message="来自服务端的报错消息：\n" + response.Error["Message"])
                            else:
                                return_type: AbstrackType = self.config.types.typesByName.get(response.ResultType)
                                if return_type is None:
                                    raise TrackException(code=ExceptionCode.Core,
                                                         message="对应的{0}类型的抽象类型尚未注册"
                                                         .format(response.ResultType))
                                return return_type.deserialize(response.Result)
                finally:
                    del self.task[request.Id]
            return None
        return invoke
