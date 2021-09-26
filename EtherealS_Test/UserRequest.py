from Request.Decorator.Request import Request
from EtherealS_Test.User import User


class UserRequest:

    @Request()
    def Register(self, username: str, id: int) -> bool:
        pass

    @Request()
    def SendSay(self,listener_id: int ,message: str) -> bool:
        pass

    @Request()
    def Add(self,a: int,b: int) -> int:
        pass
