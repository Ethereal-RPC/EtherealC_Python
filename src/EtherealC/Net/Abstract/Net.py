from abc import ABC, abstractmethod
from enum import Enum

from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Core.Model.AbstractType import AbstrackType
from EtherealC.Net.WebSocket.WebSocketNetConfig import WebSocketNetConfig
from EtherealC.Service.Abstract.Service import Service
from EtherealC.Core.Event import Event


class NetType(Enum):
    WebSocket = 1


class Net(ABC):
    def __init__(self, name):
        self.name = name
        self.config = None
        self.services = dict()
        self.requests = dict()
        self.exception_event = Event()
        self.log_event = Event()
        self.type = None

    def ServerRequestReceiveProcess(self, request: ServerRequestModel):
        service: Service = self.services.get(request.Service)
        if service is not None:
            method: classmethod = service.methods.get(request.MethodId, None)
            if method is not None:
                params_id = request.MethodId.split("-")
                for i in range(1, params_id.__len__()):
                    rpc_type: AbstrackType = service.types.typesByName.get(params_id[i], None)
                    request.Params[i-1] = rpc_type.deserialize(request.Params[i-1])
                result = method.__call__(*request.Params)
            else:
                raise TrackException(code=ExceptionCode.NotFoundService,
                                     message="未找到方法{0}-{1}-{2}".format(self.name, request.Service,
                                                                       request.MethodId))
        else:
            raise TrackException(code=ExceptionCode.NotFoundService, message="未找到服务{0}-{1}".format(self.name, request.Service))

    def ClientResponseReceiveProcess(self, response: ClientResponseModel):
        request = self.requests.get(response.Service)
        if request is None:
            raise TrackException(code=ExceptionCode.Runtime,
                                 message="未找到请求{0}-{1}".format(self.name, response.Service))
        model: ClientRequestModel = request.task.get(response.Id)
        if model is not None:
            model.Set(response)
        else:
            raise TrackException(code=ExceptionCode.Runtime,
                                 message="{0}-{1}-{2}返回的请求ID未找到".format(self.name, response.Service, response.Id))


    @abstractmethod
    def Publish(self):
        pass

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
