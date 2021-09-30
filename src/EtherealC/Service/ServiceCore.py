from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net import NetCore
from EtherealC.Net.Abstract.Net import Net, NetType
from EtherealC.Service.Abstract.Service import Service
from EtherealC.Service.WebSocket.WebSocketService import WebSocketService
from EtherealC.Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


def Get(**kwargs):
    net_name = kwargs.get("name")
    service_name = kwargs.get("name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(service_name, None)


def Register(net, service):
    if net.services.get(service.name, None) is None:
        from EtherealC.Service import Abstract
        Abstract.Service.register(service)
        net.services[service.name] = service
        service.net_name = net.name
        service.log_event.register(net.OnLog)
        service.exception_event.register(net.OnException)
        return service
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(net.name, service.name))


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is not None:
        if net.services.get(service_name, None) is not None:
            del net.services[service_name]
    return True
