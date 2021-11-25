import re

from EtherealC.Core.Manager.Event.Decorator.EventSender import EventSender
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode


class EventManager:
    def __init__(self):
        self.events = dict()

    def Register(self,name,instance):
        for method_name in dir(instance):
            if not hasattr(type(instance),method_name):
                continue
            func = getattr(type(instance), method_name)
            if hasattr(func,"ethereal_event"):
                self.events[(name,func.ethereal_event.mapping)] = func

    def UnRegister(self,name,instance):
        for method_name in dir(instance):
            func = getattr(type(instance), method_name)
            if hasattr(func,"ethereal_event"):
                del self.events[(name,func.ethereal_event.mapping)]

    def Invoke(self,instance,sender:EventSender,localKwargs,context):
        func = self.events[(sender.instance,sender.method)]
        if func is None:
            raise TrackException(ExceptionCode.Runtime,"未找到{0}实例的{1}方法".format(sender.instance,sender.method))
        parameterInfos = func.__annotations__
        if func.__annotations__.__contains__("return"):
            del parameterInfos["return"]
        kwargs = dict()
        for k,v in parameterInfos.items():
            if k == "event_context":
                kwargs[k] = context
            elif sender.paramsMapping.__contains__(k):
                kwargs[k] = localKwargs[sender.paramsMapping[k]]
            else:
                raise TrackException(ExceptionCode.Core, "调用{0}实例的{1}方法时，未提供{2}参数映射".format(sender.instance, sender.method,k))
        func(instance,**kwargs)