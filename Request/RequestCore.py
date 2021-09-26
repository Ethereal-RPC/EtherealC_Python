from Core.Model.TrackException import TrackException, ExceptionCode

from Request.Abstract.RequestConfig import RequestConfig
from Request.WebSocket.WebSocketRequest import WebSocketRequest
from Request.WebSocket.WebSocketRequestConfig import WebSocketRequestConfig

def Get(**kwargs):
    from Net.Abstract.Net import Net
    from Net import NetCore
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    request = net.requests.get(request_name)
    if request is not None:
        return request.instance
    return None


def GetRequest(**kwargs):
    from Net.Abstract.Net import Net
    from Net import NetCore
    net_name = kwargs.get("net_name")
    request_name = kwargs.get("service_name")
    if net_name is not None:
        net: Net = NetCore.Get(net_name)
    else:
        net: Net = kwargs.get("net")
    if net is None:
        return None
    return net.requests.get(request_name)


def Register(instance, net, service_name, types=None, config=None):
    from Net.Abstract.Net import NetType
    if config is None:
        if net.type == NetType.WebSocket:
            config: RequestConfig = WebSocketRequestConfig(types)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Request-Register处理".format(net.type))
    if net.requests.get(service_name, None) is None:
        if net.type == NetType.WebSocket:
            request = WebSocketRequest(config)
        else:
            raise TrackException(ExceptionCode.Core, "未有针对{0}的Request-Register处理".format(net.type))
        request.register(instance, net.net_name, service_name, config)
        net.requests[service_name] = request
        request.log_event.register(net.OnLog)
        request.exception_event.register(net.OnException)
    else:
        raise TrackException(ExceptionCode.Core, "{0}-{1}已注册，无法重复注册！".format(net.net_name, service_name))
    return instance


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        from Net import NetCore
        net = NetCore.Get(net_name)
    else:
        net = kwargs.get("net")
    if net is not None:
        if net.requests.get(service_name, None) is not None:
            del net.requests[service_name]
    return True
