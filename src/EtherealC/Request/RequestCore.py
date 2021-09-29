from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode

from EtherealC.Request.Abstract.RequestConfig import RequestConfig
from EtherealC.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealC.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


def Get(**kwargs):
    from EtherealC.Net.Abstract.Net import Net
    from EtherealC.Net import NetCore
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.requests.get(request_name, None)


def Register(instance, net, service_name, types, config=None):
    if net.requests.get(service_name, None) is None:
        from EtherealC.Request.Abstract import Request
        Request.register(instance, net.net_name, service_name, types, config)
        net.requests[service_name] = instance
        instance.log_event.register(net.OnLog)
        instance.exception_event.register(net.OnException)
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.net_name, service_name))
    return instance


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        from EtherealC.Net import NetCore
        net = NetCore.Get(net_name)
    else:
        net = kwargs.get("net")
    if net is not None:
        if net.requests.get(service_name, None) is not None:
            del net.requests[service_name]
    return True
