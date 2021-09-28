from random import Random
from EtherealC.Request.Abstract.Request import Request


class WebSocketRequest(Request):

    def __init__(self):
        super().__init__()
        self.random = Random()
