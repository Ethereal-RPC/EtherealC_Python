import sys
from abc import ABC
from random import Random

from EtherealC.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Request.Abstract.Request import Request

from EtherealC.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


class WebSocketRequest(Request, ABC):

    def __init__(self):
        super().__init__()
        self.config = WebSocketRequestConfig()
        self.random = Random()

