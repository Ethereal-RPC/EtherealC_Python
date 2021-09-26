import threading
import time

from Core.Model.AbstractTypes import AbstractTypes
from Core.Model.TrackException import TrackException, ExceptionCode
from Net.Abstract.Net import Net, NetType


class WebSocketNet(Net):
    def __init__(self, net_name):
        super().__init__(net_name=net_name)
        self.connectSign = threading.Event()

    def Publish(self):
        if self.config.netNodeMode is True:
            from Net import NetCore
            types = AbstractTypes()
            types.add(type=int, type_name="Int")
            from Net.NetNodeClient.Model.NetNode import NetNode
            types.add(type=type(NetNode()), type_name="NetNode")
            types.add(type=str, type_name="String")
            types.add(type=bool, type_name="Bool")
            from Service import ServiceCore
            from Net.NetNodeClient.Service.ClientNetNodeService import ClientNetNodeService
            netNodeService = ServiceCore.Register(net=self, instance=ClientNetNodeService(),
                                                  service_name="ClientNetNodeService", types=types)
            from Request import RequestCore
            from Net.NetNodeClient.Request.ServerNetNodeRequest import ServerNetNodeRequest
            netNodeRequest = RequestCore.Register(net=self, instance=ServerNetNodeRequest(),
                                                  service_name="ServerNetNodeService", types=types)
            from twisted.internet import reactor

            def NetNodeSearchRunner():
                try:
                    while True:
                        self.NetNodeSearch()
                        self.connectSign.wait(timeout=self.config.netNodeHeartbeatCycle/1000)
                        self.connectSign.clear()
                except Exception as exception:
                    self.OnException(
                        TrackException(exception=exception, message="NetNodeSearch循环报错", code=ExceptionCode.Runtime))

            reactor.callInThread(NetNodeSearchRunner)
            reactor.run()
        else:
            try:
                for request in self.requests.values():
                    request.client.Connect()
            except Exception as e:
                self.OnException(exception=TrackException(exception=e))
        return True

    def NetNodeSearch(self):
        flag = False
        for request in self.requests.values():
            if request.client is None and request.service_name != "ServerNetNodeService":
                flag = True
                break
        if flag is True:
            for item in self.config.netNodeIps:
                prefixes = item["prefixes"]
                config = item["config"]
                from Client import ClientCore
                client = ClientCore.Register(net=self, service_name="ServerNetNodeService", prefixes=prefixes,
                                             config=config)
                try:
                    client.Connect()
                    if client.IsConnect():
                        from Request import RequestCore
                        from Net.NetNodeClient.Request.ServerNetNodeRequest import ServerNetNodeRequest
                        netNodeRequest: ServerNetNodeRequest = RequestCore.Get(net=self, service_name="ServerNetNodeService")
                        if netNodeRequest is None:
                            raise TrackException(code=ExceptionCode.Runtime, message="无法找到{0}-ServerNetNodeService"
                                                 .format(self.net_name))
                        for request in self.requests.values():
                            if request.client is not None:
                                continue
                            node = netNodeRequest.GetNetNode(request.service_name)
                            if node is None:
                                raise TrackException(code=ExceptionCode.Runtime,
                                                     message="{0}-{1}-在NetNode分布式中未找到节点"
                                                     .format(self.net_name, request.service_name))
                            requestClient = ClientCore.Register(net=self, service_name=request.service_name, prefixes=node.Prefixes[0])
                            requestClient.disconnect_event.register(self.ClientConnectFailEvent)
                            requestClient.Connect()
                        return
                finally:
                    ClientCore.UnRegister(net=self, service_name="ServerNetNodeService")

    def ClientConnectFailEvent(self, client):
        from Client import ClientCore
        ClientCore.UnRegister(net=self, service_name=client.service_name)
        self.connectSign.set()
