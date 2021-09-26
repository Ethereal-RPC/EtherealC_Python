import json

from autobahn.twisted import WebSocketClientProtocol

from Core.Model.ClientResponseModel import ClientResponseModel
from Core.Model.TrackException import TrackException, ExceptionCode
from Net import NetCore


class WebSocketProtocol(WebSocketClientProtocol):
    def __init__(self):
        super().__init__()
        self.client = None

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        print("Connecting; transport details: {}".format(transport_details))
        return None  # ask for defaults

    def onOpen(self):
        from Client.Abstract.Client import Client
        self.client: Client = self.factory
        self.client.handle = self
        self.client.OnConnect()
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            return
        else:
            net = NetCore.Get(self.client.net_name)
            if net is None:
                raise TrackException(code=ExceptionCode.Runtime, message="{0}找不到Net".format(self.net_name))
            data = payload.decode(self.client.config.encode)
            data_type = json.loads(data)["Type"]
            if data_type == "ER-1.0-ClientResponse":
                response: ClientResponseModel = self.client.config.ClientResponseModelDeserialize(data)
                if response is None:
                    raise TrackException(code=ExceptionCode.Runtime, message="接收到了错误的ClientResponse:{0}".format(data))
                try:
                    from twisted.internet import reactor
                    reactor.callInThread(net.ClientResponseReceiveProcess, response)
                except Exception as e:
                    self.client.OnException(TrackException(code=ExceptionCode.Runtime, exception=e))
            elif data_type == "ER-1.0-ServerRequest":
                request = self.client.config.ServerRequestModelDeserialize(data)
                if request is None:
                    raise TrackException(code=ExceptionCode.Runtime, message="接收到了错误的ServerRequest:{0}".format(data))
                try:
                    from twisted.internet import reactor
                    reactor.callInThread(net.ServerRequestReceiveProcess, request)
                except Exception as e:
                    self.client.OnException(TrackException(code=ExceptionCode.Runtime, exception=e))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))