from EtherealC.Core.Manager.Event.Decorator.EventSender import EventSender


class ExceptionEvent(EventSender):
    def __init__(self,method):
        EventSender.__init__(self,method)
        self.isThrow = True

    def __call__(self, func):
        func.ethereal_exceptionEvent = self
        EventSender.__call__(self,func)
        return func