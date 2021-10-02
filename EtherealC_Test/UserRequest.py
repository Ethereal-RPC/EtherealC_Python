from EtherealC.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealC.Request.Decorator.Request import Request


class UserRequest(WebSocketRequest):

    def __init__(self,name,types):
        super().__init__()
        self.name = name
        self.types = types

    @Request()
    def Register(self, username: str, id: int) -> bool:
        pass

    @Request()
    def SendSay(self, listener_id: int, message: str) -> bool:
        pass

    @Request()
    def Add(self, a: int, b: int) -> int:
        pass
