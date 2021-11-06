from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Request.Abstract.Request import Request

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


def Register(net, request):
    if net.requests.get(request.name, None) is None:
        from EtherealC.Request.Abstract import Request
        Request.register(request)
        net.requests[request.name] = request
        request.net = net
        request.log_event.register(net.OnLog)
        request.exception_event.register(net.OnException)
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.name, request.name))
    return request


def UnRegister(request: Request):
    if request.net.requests.get(request.name, None) is not None:
        del request.net.requests[request.name]
    request.net = None
    return True
