from EtherealC.Core.Event import Event
from EtherealC.Core.Model.TrackException import TrackException
from EtherealC.Core.Model.TrackLog import TrackLog


class BaseCore:
    def __init__(self):
        self.exception_event = Event()
        self.log_event = Event()
        self.isRegister = False

    def OnLog(self, log: TrackLog = None, code=None, message=None):
        if log is None:
            log = TrackLog(code=code, message=message)
        log.sender = self
        self.log_event.onEvent(log=log)

    def OnException(self, exception: TrackException = None, code=None, message=None):
        if exception is None:
            exception = TrackException(code=code, message=message)
        exception.sender = self
        self.exception_event.onEvent(exception=exception)