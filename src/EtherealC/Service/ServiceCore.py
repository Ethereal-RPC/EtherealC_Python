from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net import NetCore
from EtherealC.Net.Abstract.Net import Net, NetType
from EtherealC.Service.Abstract.Service import Service
from EtherealC.Service.WebSocket.WebSocketService import WebSocketService
from EtherealC.Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


def Get(service_name, net=None, net_name=None):
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    if net is None:
        return None
    return net.services.get(service_name, None)


def Register(net, service):
    if net.services.get(service.name, None) is None:
        from EtherealC.Service import Abstract
        Abstract.Service.register(service)
        net.services[service.name] = service
        service.net = net
        service.log_event.register(net.OnLog)
        service.exception_event.register(net.OnException)
        return service
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(net.name, service.name))


def UnRegister(service: Service):
    if service.net.services.get(service.name, None) is not None:
        del service.net.services[service.name]
    service.net = None
    return True
