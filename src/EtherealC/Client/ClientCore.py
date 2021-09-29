from EtherealC.Client.WebSocket.WebSocketClientConfig import WebSocketClientConfig
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Client.Abstract import Client
from EtherealC.Net import NetCore
from EtherealC.Net.Abstract.Net import Net, NetType
from EtherealC.Client.WebSocket.WebSocketClient import WebSocketClient
from EtherealC.Request import RequestCore


def Get(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net = NetCore.Get(net_name)
    else:
        net = kwargs.get("net")
    if service_name is not None:
        request = RequestCore.Get(net=net, service_name=service_name)
    else:
        request = kwargs.get("request")
    if request is not None:
        return request.client
    else:
        return None


def Register(**kwargs) -> Client:
    net: Net = kwargs.get("net")
    service_name = kwargs.get("service_name")
    prefixes = kwargs.get("prefixes")
    config = kwargs.get("config")
    request = kwargs.get("request")
    if request is None:
        request = RequestCore.Get(net=net, service_name=service_name)
    if config is None:
        config = WebSocketClientConfig()
    if request is None:
        raise TrackException(ExceptionCode.Core, "未找到{0}-{1}请求".format(net.type, service_name))
    if net.type == NetType.WebSocket:
        request.client = WebSocketClient(net_name=net.net_name, service_name=request.service_name, prefixes=prefixes,
                                         config=config)
    else:
        raise TrackException(ExceptionCode.Core, "未有针对{0}的Server-Register处理".format(net.type))

    def onLog(**kwargs):
        net.OnLog(**kwargs)

    request.client.log_event.register(net.OnLog)
    request.client.exception_event.register(net.OnException)
    request.client.connectSuccess_event.register(request.OnConnectSuccess)
    return request.client


def UnRegister(**kwargs):
    net_name = kwargs.get("net_name")
    service_name = kwargs.get("service_name")
    if net_name is not None:
        net = NetCore.Get(net_name)
    else:
        net = kwargs.get("net")
    if service_name is not None:
        request = RequestCore.Get(net=net, service_name=service_name)
    else:
        request = kwargs.get("request")
    if request.client is not None:
        request.client.DisConnect()
        request.client = None
    return True
