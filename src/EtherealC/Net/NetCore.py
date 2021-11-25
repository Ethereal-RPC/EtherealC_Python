from EtherealC.Client import ClientCore
from EtherealC.Request import RequestCore
from EtherealC.Service import ServiceCore
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net.Abstract.Net import Net

nets = dict()


def Get(name) -> Net:
    return nets.get(name)


def Register(net: Net) -> Net:
    if not net.isRegister:
        net.isRegister = True
        nets[net.name] = net
    else:
        raise TrackException(code=ExceptionCode.Core,message="Net:{0}已注册".format(net.name))
    return nets[net.name]


def UnRegister(net):
    if net.isRegister:
        if nets.__contains__(net.name):
            del nets[net.name]
        net.isRegister = False
        return True
    else:
        raise TrackException(ExceptionCode.Core,"{0}已经UnRegister".format(net.name))