import sys
from abc import ABC, abstractmethod

from EtherealC.Core.BaseCore.MZCore import MZCore
from EtherealC.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealC.Core.Manager.AbstractType.AbstractTypeManager import AbstractTypeManager
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Core.Event import Event
from EtherealC.Request.Decorator.Request import Request


def register(instance):
    from EtherealC.Request.Decorator.RequestMapping import RequestMapping
    for method_name in dir(instance):
        if not hasattr(instance, method_name):
            continue
        func = getattr(instance, method_name)
        if hasattr(func,"ethereal_requestMapping"):
            if func.__annotations__.__contains__("return"):
                parameterInfos = func.__annotations__
            else:
                raise TrackException(ExceptionCode.Core, "请定义{0}方法的返回值".format(func.__name__))
            for (k,v) in parameterInfos.items():
                if k == "return" and v is None:
                    continue
                elif instance.types.typesByType.get(v, None) is not None:
                    parameterInfos[k] = instance.types.typesByType.get(v, None)
                elif instance.types.typesByName.get(k, None) is not None:
                    parameterInfos[k] = instance.types.typesByName.get(k, None)
                if parameterInfos[k] is v:
                    raise TrackException(code=ExceptionCode.Core, message="{0}方法{1}参数对应的{2}类型的抽象类型尚未注册"
                                         .format(func.__name__, k, parameterInfos[k]))


@Request()
class Request(ABC,MZCore):

    def __init__(self):
        MZCore.__init__(self)
        self.config = None
        self.name = None
        self.net = None
        self.connectSuccess_event = Event()
        self.task = dict()
        self.services = dict()
        self.client = None

    def OnConnectSuccess(self):
        self.connectSuccess_event.onEvent(request=self)

    @abstractmethod
    def Initialize(self):
        pass

    @abstractmethod
    def Register(self):
        pass

    @abstractmethod
    def UnRegister(self):
        pass

    @abstractmethod
    def UnInitialize(self):
        pass

    def ClientResponseReceiveProcess(self, response: ClientResponseModel):
        model: ClientRequestModel = self.task.get(response.Id)
        if model is not None:
            model.Set(response)
        else:
            raise TrackException(code=ExceptionCode.Runtime,
                                 message="{0}-{1}返回的请求ID未找到".format(self.name, response.Id))