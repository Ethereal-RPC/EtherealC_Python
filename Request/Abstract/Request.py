from abc import ABC
from Core.Model.TrackException import TrackException
from Core.Model.TrackLog import TrackLog
from Request.Abstract.RequestConfig import RequestConfig
from Core.Event import Event


class Request(ABC):

    def __init__(self, config: RequestConfig):
        self.config = config
        self.service_name = None
        self.net_name = None
        self.exception_event = Event()
        self.log_event = Event()
        self.connectSuccess_event = Event()
        self.client = None
        self.task = dict()
        self.instance = None

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
        self.connectSuccess_event.onEvent(request=self.instance)
