from EtherealC.Core.Manager.Event.Decorator.EventSender import EventSender


class AfterEvent(EventSender):
    def __init__(self,method):
        EventSender.__init__(self,method)

    def __call__(self, func):
        func.ethereal_afterEvent = self
        EventSender.__call__(self,func)
        return func