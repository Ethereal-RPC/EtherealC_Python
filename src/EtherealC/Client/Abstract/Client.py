from abc import ABC, abstractmethod

from EtherealC.Core.BaseCore.BaseCore import BaseCore
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.TrackException import TrackException
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Client.Abstract.ClientConfig import ClientConfig
from EtherealC.Core.Event import Event
from EtherealC.Request.Abstract.Request import Request


class Client(ABC,BaseCore):

    def __init__(self, prefixes):
        BaseCore.__init__(self)
        self.config = None
        self.prefixes: str = prefixes
        self.request: Request = None
        self.exception_event = Event()
        self.log_event = Event()
        self.connectSuccess_event = Event()
        self.connectFail_event = Event()
        self.disconnect_event = Event()

    @abstractmethod
    def Connect(self):
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

    def OnConnectSuccess(self):
        self.connectSuccess_event.onEvent(client=self)

    def OnDisConnect(self):
        self.disconnect_event.onEvent(client=self)

    def OnConnectFail(self):
        self.connectFail_event.onEvent(client=self)

    @abstractmethod
    def SendClientRequestModel(self, request: ClientRequestModel):
        pass
