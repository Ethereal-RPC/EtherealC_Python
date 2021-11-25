import json

from autobahn.twisted import WebSocketClientProtocol

from EtherealC.Client.Abstract.Client import Client
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net import NetCore


class WebSocketProtocol(WebSocketClientProtocol):
    def __init__(self):
        super().__init__()
        self.client: Client = None

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        print("Connecting; transport details: {}".format(transport_details))
        return None  # ask for defaults

    def onOpen(self):
        from EtherealC.Client.WebSocket.WebSocketClient import WebSocketClient
        self.client: WebSocketClient = self.factory
        self.client.handle = self
        self.client.syncSign.set()
        self.client.syncSign.clear()
        self.client.OnConnectSuccess()

    def onMessage(self, payload, isBinary):
        if isBinary:
            return
        else:
            data = payload.decode(self.client.config.encode)
            data_type = json.loads(data)["Type"]
            if data_type == "ER-1.0-ClientResponse":
                response: ClientResponseModel = self.client.config.ClientResponseModelDeserialize(data)
                if response is None:
                    raise TrackException(code=ExceptionCode.Runtime, message="接收到了错误的ClientResponse:{0}".format(data))
                try:
                    from twisted.internet import reactor
                    reactor.callInThread(self.client.request.ClientResponseReceiveProcess, response)
                except Exception as e:
                    self.client.OnException(TrackException(code=ExceptionCode.Runtime, exception=e))
            elif data_type == "ER-1.0-ServerRequest":
                request: ServerRequestModel = self.client.config.ServerRequestModelDeserialize(data)
                if request is None:
                    raise TrackException(code=ExceptionCode.Runtime, message="接收到了错误的ServerRequest:{0}".format(data))
                try:
                    from twisted.internet import reactor
                    if not self.client.request.services.__contains__(request.Service):
                        raise TrackException(code=ExceptionCode.Runtime,
                                             message="找不到Service:{0}".format(request.Service))
                    reactor.callInThread(self.client.request.services[request.Service].ServerRequestReceiveProcess, request)
                except Exception as e:
                    self.client.OnException(TrackException(code=ExceptionCode.Runtime, exception=e))