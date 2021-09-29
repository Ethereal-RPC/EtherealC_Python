import sys
from random import Random

from EtherealC.Core.Model.AbstractType import AbstrackType
from EtherealC.Request.Abstract.Request import Request
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode

from EtherealC.Request.Decorator.Request import RequestAnnotation
from EtherealC.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


class WebSocketRequest(Request):

    def __init__(self):
        super().__init__()
        self.config = WebSocketRequestConfig()
        self.random = Random()

    def getInvoke(self, method, method_id, return_name, annotation: RequestAnnotation):
        def invoke(*args, **kwargs):
            from EtherealC.Request.Decorator import InvokeTypeFlags
            localResult = None
            remoteResult = None
            if (annotation.invokeType & InvokeTypeFlags.Local) == 0:
                parameters = list()
                parameters.append(None)
                for arg in args:
                    abstract_type: AbstrackType = self.types.typesByType.get(type(arg), None)
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
                                    if (annotation.invokeType & InvokeTypeFlags.Fail) != 0:
                                        localResult = method(*args, **kwargs)
                                    else:
                                        raise TrackException(code=ExceptionCode.Runtime,
                                                             message="来自服务端的报错消息：\n" + response.Error["Message"])
                                else:
                                    return_type: AbstrackType = self.types.typesByName.get(response.ResultType)
                                    if return_type is None:
                                        raise TrackException(code=ExceptionCode.Core,
                                                             message="对应的{0}类型的抽象类型尚未注册"
                                                             .format(response.ResultType))
                                    remoteResult = return_type.deserialize(response.Result)
                                    if (annotation.invokeType & InvokeTypeFlags.Success) != 0 or (annotation.invokeType & InvokeTypeFlags.All) != 0 :
                                        localResult = method(*args, **kwargs)
                            elif (annotation.invokeType & InvokeTypeFlags.Timeout) != 0:
                                localResult = method(*args, **kwargs)
                    finally:
                        del self.task[request.Id]
            else:
                localResult = method(*args, **kwargs)
            if (annotation.invokeType & InvokeTypeFlags.Remote) != 0:
                return remoteResult
            elif (annotation.invokeType & InvokeTypeFlags.Local) != 0:
                return localResult
            return remoteResult
        return invoke
