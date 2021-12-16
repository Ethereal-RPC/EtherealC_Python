from numbers import Number

from EtherealC.Client.WebSocket.WebSocketClient import WebSocketClient
from EtherealC.Net.WebSocket.WebSocketNet import WebSocketNet
from EtherealC.Request.Decorator import InvokeTypeFlags
from EtherealC_Test.User import User
from EtherealC_Test.UserRequest import UserRequest
from EtherealC_Test.UserService import UserService
from EtherealC.Net.Abstract.Net import NetType
from EtherealC.Client import ClientCore
from EtherealC.Net import NetCore
from EtherealC.Request import RequestCore
from EtherealC.Service import ServiceCore


def OnException(exception):
    raise exception.exception


def OnLog(log):
    print(log)


def Single():
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
    # 建立网关
    net = NetCore.Register(WebSocketNet("demo"))
    net.exception_event.Register(OnException)
    net.log_event.Register(OnLog)
    # 注册请求
    request: UserRequest = RequestCore.Register(net=net, request=UserRequest())
    # 注册服务
    service = ServiceCore.Register(request=request, service=UserService())
    service.userRequest = request
    # 注册连接
    client = ClientCore.Register(request=request, client=WebSocketClient(prefixes=prefixes),isConnect=False)
    request.connectSuccess_event.Register(requestConnect)
    client.disconnect_event.Register(disconnect)
    client.Connect()
    net.Publish()
    print("服务器初始化完成....")


def requestConnect(request=None):
    print("---------------------------")
    print("执行Add请求:")
    print("2+3={0}".format(request.Add(2,3)))
    print("---------------------------")
    print("执行Login请求:")
    print(request.Login("Python"))
    print("---------------------------")
    print("执行Hello请求:")
    print(request.Hello())
    print("---------------------------")


def disconnect(client=None):
    print("连接失败")


if __name__ == '__main__':
    Single()
    # NetNode()

