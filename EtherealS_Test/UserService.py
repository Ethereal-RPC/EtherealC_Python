from numbers import Number

from Service.Decorator.Service import Service
from EtherealS_Test.User import User


class UserService:
    def __init__(self):
        self.userRequest = None

    @Service()
    def Say(self, sender: User, message: str):
        print(sender.UserName + ":" + message)
