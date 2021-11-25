from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Request.Abstract.Request import Request

from EtherealC.Request.Abstract.RequestConfig import RequestConfig
from EtherealC.Request.WebSocket.WebSocketRequest import WebSocketRequest
from EtherealC.Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig


def Get(net_name=None, request_name=None, net=None):
    from EtherealC.Net.Abstract.Net import Net
    from EtherealC.Net import NetCore
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    if net is None:
        return None
    return net.requests.get(request_name, None)


def Register(net, request:Request):
    if not request.isRegister:
        request.isRegister = True
        request.Initialize()
        import EtherealC.Request.Abstract.Request as RequestStatic
        RequestStatic.register(request)
        net.requests[request.name] = request
        request.net = net
        request.Register()
        request.log_event.Register(net.OnLog, )
        request.exception_event.Register(net.OnException, )
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.name, request.name))
    return request


def UnRegister(request: Request):
    if request.isRegister:
        request.UnRegister()
        if request.net.requests.__contains__(request.name):
            del request.net.requests[request.name]
        request.net = None
        request.isRegister = False
        request.UnInitialize()
    else:
        raise TrackException(ExceptionCode.Core,"{0}已经UnRegister".format(request.name))
