from EtherealC.Core.Manager.Event.Decorator.Event import Event
from EtherealC.Core.Manager.Event.Model.EventContext import EventContext


class EventClass:
    def __init__(self):
        self.name = "Event"

    @Event(mapping="test")
    def Test(self,s:str,d:int,event_context: EventContext):
        print(self.name)
        print(s)
        print(d)
        print(event_context)
