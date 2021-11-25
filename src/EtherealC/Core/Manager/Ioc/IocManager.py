from EtherealC.Core.Manager.Event.Decorator.EventSender import EventSender
from EtherealC.Core.Manager.Event.EventManager import EventManager
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode


class IocManager:
    def __init__(self):
        self._iocContainer = dict()
        self._eventManager = EventManager()

    def Register(self,name,instance):
        if self._iocContainer.get(name) is None:
            self._iocContainer[name] = instance
            self._eventManager.Register(name,instance)
        else:
            raise TrackException(ExceptionCode.Runtime,"{0}Ioc实例已经注册".format(name))

    def UnRegister(self,name):
        if self._iocContainer.get(name) is not None:
            instance = self._iocContainer[name]
            self._eventManager.UnRegister(name, instance)
            del self._iocContainer[name]

    def Get(self,name):
        return self._iocContainer[name]

    def InvokeEvent(self,sender:EventSender,localKwargs,context):
        self._eventManager.Invoke(self._iocContainer[sender.instance],sender,localKwargs,context)