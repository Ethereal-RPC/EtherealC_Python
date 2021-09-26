import json

from Core.Model import ClientRequestModel
from Core.Model.ClientResponseModel import ClientResponseModel
from Core.Model import ServerRequestModel
from Client.Abstract.ClientConfig import ClientConfig
from Utils.JsonTool import JSONClientResponseModel


class WebSocketClientConfig(ClientConfig):

    def __init__(self):
        super(WebSocketClientConfig, self).__init__()
        self.threadCount = 5
        self.connectTimeout = 6000
