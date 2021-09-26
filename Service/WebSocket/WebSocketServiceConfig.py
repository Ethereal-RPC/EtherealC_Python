from Core.Model.AbstractTypes import AbstractTypes
from Service.Abstract import Service
from Service.Abstract.ServiceConfig import ServiceConfig


class WebSocketServiceConfig(ServiceConfig):

    def __init__(self, _type: AbstractTypes):
        super().__init__(_type)
