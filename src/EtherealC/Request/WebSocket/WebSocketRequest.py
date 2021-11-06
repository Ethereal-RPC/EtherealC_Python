import sys
from abc import ABC
from random import Random

from EtherealC.Core.Model.AbstractType import AbstrackType
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Request.Abstract.Request import Request

from EtherealC.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


class WebSocketRequest(Request, ABC):

    def __init__(self):
        super().__init__()
        self.config = WebSocketRequestConfig()
        self.random = Random()

    from EtherealC.Request.Decorator.RequestMethod import RequestMethod

    def getInvoke(self, func, annotation: RequestMethod):
        def invoke(*args, **kwargs):
            from EtherealC.Request.Decorator import InvokeTypeFlags
            localResult = None
            remoteResult = None
            if (annotation.invokeType & InvokeTypeFlags.Local) == 0:
                method_id: str = func.__name__
                params = list()
                if func.__annotations__.get("return") is not None:
                    parameterInfos = list(func.__annotations__.values())[:-1:]
                else:
                    parameterInfos: list = list(func.__annotations__.values())
                for i in range(0, parameterInfos.__len__()):
                    abstractType: AbstrackType = self.types.typesByType.get(parameterInfos[i], None)
                    if abstractType is None:
                        raise TrackException(code=ExceptionCode.Core, message="对应的{0}类型的抽象类型尚未注册"
                                             .format(parameterInfos[i]))
                    method_id += "-" + abstractType.name
                    params.append(abstractType.serialize(args[i]))
                request = ClientRequestModel(method_id=method_id, params=params, service=self.name)
                if func.__annotations__.get("return") is None:
                    self.net.client.SendClientRequestModel(request)
                else:
                    request.Id = str(self.random.randint(0, sys.maxsize))
                    while self.task.get(request.Id) is not None:
                        request.Id = str(self.random.randint(0, sys.maxsize))
                    self.task[request.Id] = request
                    try:
                        timeout = annotation.timeout
                        if timeout is not None:
                            timeout = self.config.timeout
                        if self.net.client.SendClientRequestModel(request):
                            response: ClientResponseModel = request.Get(timeout)
                            if response is not None:
                                if response.Error is not None:
                                    if (annotation.invokeType & InvokeTypeFlags.Fail) != 0:
                                        localResult = func(*args, **kwargs)
                                    else:
                                        raise TrackException(code=ExceptionCode.Runtime,
                                                             message="来自服务端的报错消息：\n" + response.Error["Message"])
                                else:
                                    return_type = self.types.typesByType.get(func.__annotations__.get("return"))
                                    if return_type is None:
                                        raise TrackException(code=ExceptionCode.Core,
                                                             message="对应的{0}类型的抽象类型尚未注册"
                                                             .format(func.__annotations__.get("return")))
                                    remoteResult = return_type.deserialize(response.Result)
                                    if (annotation.invokeType & InvokeTypeFlags.Success) != 0 or (
                                            annotation.invokeType & InvokeTypeFlags.All) != 0:
                                        localResult = func(*args, **kwargs)
                            elif (annotation.invokeType & InvokeTypeFlags.Timeout) != 0:
                                localResult = func(*args, **kwargs)
                    finally:
                        del self.task[request.Id]
            else:
                localResult = func(*args, **kwargs)
            if (annotation.invokeType & InvokeTypeFlags.Remote) != 0:
                return remoteResult
            elif (annotation.invokeType & InvokeTypeFlags.Local) != 0:
                return localResult
            return remoteResult

        return invoke
