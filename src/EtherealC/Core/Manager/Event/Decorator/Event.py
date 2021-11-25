from EtherealC.Core.Manager.Event.Decorator.EventSender import EventSender


class Event:
    def __init__(self,mapping):
        self.mapping = mapping

    def __call__(self, func):
        func.ethereal_event = self
        return func