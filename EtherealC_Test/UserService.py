from EtherealC.Service.WebSocket.WebSocketService import WebSocketService
from EtherealC.Service.Decorator.ServiceMethod import ServiceMethod
from EtherealC_Test.User import User


class UserService(WebSocketService):

    def Initialize(self):
        pass

    def UnInitialize(self):
        pass

    def __init__(self, name, types):
        super().__init__()
        self.name = name
        self.types = types
        self.userRequest = None

    @ServiceMethod()
    def Say(self, sender: User, message: str):
        print(sender.Username + ":" + message)
