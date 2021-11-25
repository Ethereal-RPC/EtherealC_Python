from EtherealC.Client.Abstract import Client
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net import NetCore
from EtherealC.Net.Abstract.Net import Net
from EtherealC.Request import RequestCore
from EtherealC.Request.Abstract.Request import Request


def Get(net_name = None, request_name = None, net = None):
    request = RequestCore.Get(net_name=net_name, request_name=request_name,net = net)
    if request is not None:
        return request.client
    return None


def Register(client: Client, request: Request, isConnect=True) -> Client:
    if not client.isRegister:
        client.isRegister = True
        request.client = client
        client.request = request
        client.log_event.Register(request.OnLog )
        client.exception_event.Register(request.OnException )
        client.connectSuccess_event.Register(OnConnectSuccess)
        if isConnect:
            client.Connect()
    return client


def OnConnectSuccess(client):
        client.request.OnConnectSuccess()


def UnRegister(client):
    if client.isRegister:
        if client.request is not None:
            client.request.client = None
            client.request = None
        client.DisConnect()
        client.isRegister = False
        return True
    else:
        raise TrackException(ExceptionCode.Core,"{0}已经UnRegister".format(client.name))
