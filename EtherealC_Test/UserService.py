from numbers import Number

from EtherealC.Service.WebSocket.WebSocketService import WebSocketService
from EtherealC.Service.Decorator.ServiceMapping import ServiceMapping
from EtherealC_Test.EventClass import EventClass
from EtherealC_Test.User import User


class UserService(WebSocketService):

    def Initialize(self):
        self.name = "Client"
        self.types.add(type=int, type_name="Int")
        self.types.add(type=type(User()), type_name="User")
        self.types.add(type=Number, type_name="Number")
        self.types.add(type=str, type_name="String")
        self.types.add(type=bool, type_name="Bool")
        self.iocManager.Register("instance", EventClass())

    def Register(self):
        pass

    def UnRegister(self):
        pass

    def UnInitialize(self):
        pass

    @ServiceMapping("Say")
    def Say(self, sender: User, message: str) -> None:
        print(sender.Username + ":" + message)