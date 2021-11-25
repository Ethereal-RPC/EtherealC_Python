from EtherealC.Core.Manager.Event.Decorator.EventSender import EventSender


class SuccessEvent(EventSender):
    def __init__(self,method):
        EventSender.__init__(self,method)
        self.isThrow = False

    def __call__(self, func):
        func.ethereal_successEvent = self
        EventSender.__call__(self,func)
        return func