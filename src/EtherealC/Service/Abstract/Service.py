from abc import ABC, abstractmethod

from EtherealC.Core.BaseCore.BaseCore import BaseCore
from EtherealC.Core.BaseCore.MZCore import MZCore
from EtherealC.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealC.Core.Manager.AbstractType.AbstractTypeManager import AbstractTypeManager

from EtherealC.Core.Manager.Event.Model.EventContext import EventContext
from EtherealC.Core.Manager.Ioc.IocManager import IocManager
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Core.Model.TrackLog import TrackLog
from EtherealC.Service.Abstract import ServiceConfig
from EtherealC.Core import Event
from EtherealC.Service.Decorator.Service import Service


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
                if k == "return":
                    continue
                elif instance.types.typesByType.get(v, None) is not None:
                    parameterInfos[k] = instance.types.typesByType.get(v, None)
                elif instance.types.typesByName.get(k, None) is not None:
                    parameterInfos[k] = instance.types.typesByName.get(k, None)
                if parameterInfos[k] is not AbstrackType:
                    raise TrackException(code=ExceptionCode.Core, message="{0}方法{1}参数对应的{2}类型的抽象类型尚未注册"
                                         .format(func.__name__, k, parameterInfos[k]))


@Service()
class Service(ABC,MZCore):
    def __init__(self):
        MZCore.__init__(self)
        self.config: ServiceConfig = None
        self.methods = dict()
        self.request = None
        self.name = None
        self.interceptorEvent = list()

    def OnInterceptor(self, net, method, token) -> bool:
        for item in self.interceptorEvent:
            if not item.__call__(net, self, method, token):
                return False
        return True

    def ServerRequestReceiveProcess(self, request: ServerRequestModel):
        func: classmethod = self.methods.get(request.Mapping, None)
        if func is not None:
            result = None
            kwargs = dict()
            eventContext = EventContext()
            eventContext.method = func
            parameterInfos = list(func.__annotations__.values())[:-1:]
            for parameterInfo in parameterInfos:
                abstractType = parameterInfos[parameterInfo]
                kwargs[parameterInfo] = abstractType.deserialize(request.Params[parameterInfo])
            if hasattr(func, "ethereal_beforeEvent"):
                self.iocManager.InvokeEvent(func.ethereal_beforeEvent, kwargs, eventContext)
            try:
                result = func(**kwargs)
            except Exception as e:
                if hasattr(func, "ethereal_exceptionEvent"):
                    eventContext.exception = e
                    self.iocManager.InvokeEvent(func.ethereal_exceptionEvent, kwargs, eventContext)
                    if func.ethereal_exceptionEvent.isThrow:
                        raise e
                else:
                    raise e
            if hasattr(func, "ethereal_afterEvent"):
                eventContext.result = result
                self.iocManager.InvokeEvent(func.ethereal_afterEvent, kwargs, eventContext)
        else:
            raise TrackException(code=ExceptionCode.NotFoundService,
                                 message="未找到方法{0}-{1}-{2}".format(self.name, request.Service,
                                                                   request.Mapping))

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
