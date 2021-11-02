from abc import ABC

from EtherealC.Service.Abstract.Service import Service
from EtherealC.Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


class WebSocketService(Service, ABC):
    def __init__(self):
        super().__init__()
        self.config = WebSocketServiceConfig()
