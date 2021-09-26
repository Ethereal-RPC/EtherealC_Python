from abc import ABC, abstractmethod

from Core.Model.ClientRequestModel import ClientRequestModel
from Core.Model.TrackException import TrackException
from Core.Model.TrackLog import TrackLog
from Client.Abstract.ClientConfig import ClientConfig
from Core.Event import Event


class Client(ABC):

    def __init__(self, net_name=None, service_name=None, config: ClientConfig = None):
        self.config = config
        self.net_name = net_name
        self.service_name = service_name
        self.exception_event = Event()
        self.log_event = Event()
        self.connect_event = Event()
        self.disconnect_event = Event()

    @abstractmethod
    def Connect(self):
        pass

    @abstractmethod
    def DisConnect(self):
        pass

    @abstractmethod
    def IsConnect(self):
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

    def OnConnect(self):
        self.connect_event.onEvent(client=self)

    def OnDisConnect(self):
        self.disconnect_event.onEvent(client=self)

    @abstractmethod
    def SendClientRequestModel(self, request: ClientRequestModel):
        pass
