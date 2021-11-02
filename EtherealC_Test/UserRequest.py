from EtherealC.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealC.Request.Decorator.RequestMethod import RequestMethod


class UserRequest(WebSocketRequest):

    def Initialize(self):
        pass

    def UnInitialize(self):
        pass

    def __init__(self,name,types):
        super().__init__()
        self.name = name
        self.types = types

    @RequestMethod()
    def Register(self, username: str, id: int) -> bool:
        pass

    @RequestMethod()
    def SendSay(self, listener_id: int, message: str) -> bool:
        pass

    @RequestMethod()
    def Add(self, a: int, b: int) -> int:
        pass
