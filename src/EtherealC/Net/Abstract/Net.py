from abc import ABC, abstractmethod
from enum import Enum

from EtherealC.Core.BaseCore.BaseCore import BaseCore
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealC.Service.Abstract.Service import Service
from EtherealC.Core.Event import Event


class NetType(Enum):
    WebSocket = 1


class Net(ABC,BaseCore):
    def __init__(self, name):
        BaseCore.__init__(self)
        ABC.__init__(self)
        self.name = name
        self.config = None
        self.requests = dict()
        self.type = None

    @abstractmethod
    def Publish(self):
        pass
