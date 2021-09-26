from Core.Model.AbstractTypes import AbstractTypes
from Request.Abstract.RequestConfig import RequestConfig


class WebSocketRequestConfig(RequestConfig):

    def __init__(self, config_type: AbstractTypes):
        super().__init__(config_type)


