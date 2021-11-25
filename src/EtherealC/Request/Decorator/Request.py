from enum import Enum

from EtherealC.Request.Decorator import InvokeTypeFlags


class Request:
    def __init__(self):
        pass

    def __call__(self, func):
        func.ethereal_request = self
        return func
