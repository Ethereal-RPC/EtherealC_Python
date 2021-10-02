from EtherealC.Service.WebSocket.WebSocketService import WebSocketService
from EtherealC.Service.Decorator.Service import Service
from EtherealC_Test.User import User


class UserService(WebSocketService):

    def __init__(self, name, types):
        super().__init__()
        self.name = name
        self.types = types
        self.userRequest = None

    @Service()
    def Say(self, sender: User, message: str):
        print(sender.UserName + ":" + message)
