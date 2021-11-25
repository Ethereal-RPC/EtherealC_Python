from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net import NetCore
from EtherealC.Net.Abstract.Net import Net, NetType
from EtherealC.Request import RequestCore
from EtherealC.Service.Abstract.Service import Service
from EtherealC.Service.WebSocket.WebSocketService import WebSocketService
from EtherealC.Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


def Get(service_name, net=None, net_name=None,request_name = None):
    request = RequestCore.Get(net_name=net_name, request_name=request_name,net = net)
    if request is not None:
        return request.services.get(service_name, None)
    return None


def Register(request, service: Service):
    if not service.isRegister:
        service.isRegister = True
        service.Initialize()
        from EtherealC.Service import Abstract
        Abstract.Service.register(service)
        request.services[service.name] = service
        service.request = request
        service.log_event.Register(request.OnLog, )
        service.exception_event.Register(request.OnException, )
        service.Register()
        return service
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(request.name, service.name))


def UnRegister(service: Service):
    if service.isRegister:
        service.UnRegister()
        if service.request is not None:
            if service.net.services.__contains__(service.name):
                del service.net.services[service.name]
            service.request = None
        service.isRegister = False
        service.UnInitialize()
        return True
    else:
        raise TrackException(ExceptionCode.Core,"{0}已经UnRegister".format(service.name))
