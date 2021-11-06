from EtherealC.Client.Abstract import Client
from EtherealC.Net import NetCore
from EtherealC.Net.Abstract.Net import Net


def Get(net_name):
    net = NetCore.Get(net_name)
    if net is not None:
        return net.client
    else:
        return None


def Register(client: Client, net: Net) -> Client:
    net.client = client
    client.net = net
    client.log_event.register(net.OnLog)
    client.exception_event.register(net.OnException)
    client.connectSuccess_event.register(OnConnectSuccess)
    return client


def OnConnectSuccess(client):
    for request in client.net.requests.values():
        request.OnConnectSuccess()


def UnRegister(client):
    client.net.client = None
    client.net = None
    client.DisConnect()
    return True
