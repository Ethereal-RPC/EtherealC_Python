from numbers import Number

from EtherealC.Core.Manager.Event.Decorator.AfterEvent import AfterEvent
from EtherealC.Request.Decorator import InvokeTypeFlags
from EtherealC.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealC.Request.Decorator.RequestMapping import RequestMapping
from EtherealC_Test.EventClass import EventClass
from EtherealC_Test.User import User


class UserRequest(WebSocketRequest):

    def Initialize(self):
        self.name = "Server"
        self.types.add(type=int, type_name="Int")
        self.types.add(type=type(User()), type_name="User")
        self.types.add(type=Number, type_name="Number")
        self.types.add(type=str, type_name="String")
        self.types.add(type=bool, type_name="Bool")
        self.iocManager.Register("instance",EventClass())

    def Register(self):
        pass

    def UnRegister(self):
        pass

    def UnInitialize(self):
        pass


    @RequestMapping("Add")
    def Add(self,a: int, b: int) -> int:
        pass

    @RequestMapping("Login")
    def Login(self, username: str) -> bool:
        pass

    @RequestMapping("Hello")
    def Hello(self) -> str:
        pass

    @AfterEvent("instance.test(s:s,d:k)")
    @RequestMapping("test",invokeType=InvokeTypeFlags.Remote | InvokeTypeFlags.ReturnRemote)
    def test(self,s: str,k: int,d: int) -> bool:
        print("___________")
        print(s)
        print(k)
        print("___________")
        return False
