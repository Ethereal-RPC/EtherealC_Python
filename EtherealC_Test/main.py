from numbers import Number

from EtherealC.Client.WebSocket.WebSocketClient import WebSocketClient
from EtherealC.Net.WebSocket.WebSocketNet import WebSocketNet
from EtherealC.Request.Decorator import InvokeTypeFlags
from EtherealC_Test.User import User
from EtherealC_Test.UserRequest import UserRequest
from EtherealC_Test.UserService import UserService
from EtherealC.Core.Model.AbstractTypes import AbstractTypes
from EtherealC.Net.Abstract.Net import NetType
from EtherealC.Client import ClientCore
from EtherealC.Net import NetCore
from EtherealC.Request import RequestCore
from EtherealC.Service import ServiceCore


def OnException(**kwargs):
    from EtherealC.Core.Model.TrackException import TrackException
    exception: TrackException = kwargs.get("exception")
    raise exception.exception


def OnLog(**kwargs):
    exception = kwargs.get("log")
    print(exception)


def Single():
    port = "28015"
    print("请选择端口(0-3)")
    mode = input()
    if mode == "0":
        port = "28015"
    elif mode == "1":
        port = "28016"
    elif mode == "2":
        port = "28017"
    elif mode == "3":
        port = "28018"
    else:
        port = mode
    prefixes = "ethereal://127.0.0.1:28015/NetDemo/".replace("28015", port)
    print("Client-{0}".format(prefixes))
    types = AbstractTypes()
    types.add(type=int, type_name="Int")
    types.add(type=type(User()), type_name="User")
    types.add(type=Number, type_name="Number")
    types.add(type=str, type_name="String")
    types.add(type=bool, type_name="Bool")
    # 建立网关
    net = NetCore.Register(WebSocketNet("demo"))
    net.exception_event.register(OnException)
    net.log_event.register(OnLog)
    # 注册服务
    service = ServiceCore.Register(service=UserService(name="Client", types=types), net=net)
    # 注册请求
    request = RequestCore.Register(net=net, request=UserRequest(name="Server", types=types))
    # 突出Service为正常类
    service.userRequest = request
    # 注册连接
    client = ClientCore.Register(request=request, client=WebSocketClient(prefixes=prefixes))
    ips = list()
    # 分布式这里需要引用客户端框架，但是目前Python还没有客户端版本，暂且搁置.
    # EtherealC.NativeClient.ClientConfig clientConfig = new EtherealC.NativeClient.ClientConfig();
    net.config.netNodeMode = False
    client.connectSuccess_event.register(connect)
    client.disconnect_event.register(disconnect)
    net.Publish()
    print("服务器初始化完成....")


def NetNode():
    prefixes = "ethereal://127.0.0.1:28015/NetDemo/"
    types = AbstractTypes()
    types.add(type=int, type_name="Int")
    types.add(type=type(User()), type_name="User")
    types.add(type=Number, type_name="Number")
    types.add(type=str, type_name="String")
    types.add(type=bool, type_name="Bool")
    # 建立网关
    net = NetCore.Register(WebSocketNet("demo"))
    net.exception_event.register(OnException)
    net.log_event.register(OnLog)
    # 注册服务
    service = ServiceCore.Register(service=UserService(name="Client", types=types), net=net)
    # 注册请求
    request = RequestCore.Register(net=net, request=UserRequest(name="Server", types=types))
    # 突出Service为正常类
    service.userRequest = request
    ips = list()
    # 分布式这里需要引用客户端框架，但是目前Python还没有客户端版本，暂且搁置.
    net.config.netNodeMode = True
    from EtherealC.Client.WebSocket.WebSocketClientConfig import WebSocketClientConfig
    ips.append(dict(prefixes=prefixes.replace("28015", "28015"), config=WebSocketClientConfig()))
    ips.append(dict(prefixes=prefixes.replace("28015", "28016"), config=WebSocketClientConfig()))
    ips.append(dict(prefixes=prefixes.replace("28015", "28017"), config=WebSocketClientConfig()))
    ips.append(dict(prefixes=prefixes.replace("28015", "28018"), config=WebSocketClientConfig()))
    net.config.netNodeIps = ips
    requestProxy = RequestCore.Get(net=net, service_name="Server")
    requestProxy.connectSuccess_event.register(requestConnect)
    net.Publish()
    print("服务器初始化完成....")


def requestConnect(request=None):
    print("答案:" + str(request.Add(2, 3)))


def disconnect(client=None):
    print("连接失败")


def connect(client=None):
    request = RequestCore.Get(net_name=client.net_name, service_name=client.service_name)
    result = request.Add(2, 3)
    print("最终结果：{0}".format(result))


if __name__ == '__main__':
    Single()
    # NetNode()

