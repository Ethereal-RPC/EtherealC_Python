from Core.Model.TrackException import TrackException, ExceptionCode
from Net import NetCore
from Net.Abstract.Net import Net, NetType
from Service.Abstract.Service import Service
from Service.Abstract.ServiceConfig import ServiceConfig
from Service.WebSocket.WebSocketService import WebSocketService
from Service.WebSocket.WebSocketServiceConfig import WebSocketServiceConfig


def Get(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    service = net.services.get(service_name, None)
    if service is not None:
        return service.instance


def GetService(**kwargs) -> Service:
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.services.get(service_name, None)


def Register(instance, net, service_name, types=None, config=None):
    if config is None and types is None:
        raise TrackException(ExceptionCode.Core, "types和config必须提供一个")
    if config is None:
        if net.type == NetType.WebSocket:
            config = WebSocketServiceConfig(types)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Service-Register处理".format(net.type))

    if net.services.get(service_name, None) is None:
        if net.type == NetType.WebSocket:
            service = WebSocketService()
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Service-Register处理".format(net.type))
        service.register(net.net_name, service_name, instance, config)
        net.services[service_name] = service
        service.log_event.register(net.OnLog)
        service.exception_event.register(net.OnException)
        return service
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}Service已经注册".format(net.service_name, service_name))


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
