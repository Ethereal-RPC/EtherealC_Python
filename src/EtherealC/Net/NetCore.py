from EtherealC.Client import ClientCore
from EtherealC.Request import RequestCore
from EtherealC.Service import ServiceCore
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net.Abstract.Net import Net

nets = dict()


def Get(name) -> Net:
    return nets.get(name)


def Register(net: Net) -> Net:
    if nets.get(net.name, None) is None:
        nets[net.name] = net
    else:
        raise TrackException(code=ExceptionCode.Core,message="Net:{0}已注册".format(net.name))
    return nets[net.name]


def UnRegister(net):
    for request in net.requests:
        RequestCore.UnRegister(net_name=net, service_name=request.name)
    for service in net.services:
        ServiceCore.UnRegister(net_name=net, service_name=service.name)
    ClientCore.UnRegister(client=net.client)
    del nets[net.name]
    return True
