import sys
import threading
from urllib.parse import urlparse

from autobahn.twisted import WebSocketClientFactory

from EtherealC.Client.Abstract.Client import Client
from EtherealC.Client.WebSocket.WebSocketClientConfig import WebSocketClientConfig
from EtherealC.Client.WebSocket.WebSocketProtocol import WebSocketProtocol
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.TrackException import ExceptionCode, TrackException
from twisted.internet import reactor


class WebSocketClient(Client, WebSocketClientFactory):

    def __init__(self, prefixes):
        Client.__init__(self, prefixes=prefixes)
        WebSocketClientFactory.__init__(self, "ws://" + self.prefixes)
        self.config = WebSocketClientConfig()
        self.protocol = WebSocketProtocol
        self.handle = None
        self.syncSign = threading.Event()

    def IsConnect(self):
        while self.handle is None:
            return False
        else:
            return self.handle.is_open

    def clientConnectionLost(self, *args, **kwargs):
        super().clientConnectionLost(args, kwargs)
        self.OnDisConnect()

    def clientConnectionFailed(self, *args, **kwargs):
        super().clientConnectionFailed(args, kwargs)
        self.syncSign.set()
        self.syncSign.clear()
        self.OnConnectFail()

    def SendClientRequestModel(self, request: ClientRequestModel):
        request_body = self.config.ClientRequestModelSerialize(request)
        self.handle.sendMessage(request_body.encode(self.config.encode))
        return True

    def Connect(self, isSync=False):
        try:
            from twisted.internet import reactor
            from twisted.python import log
            log.startLogging(sys.stdout)
            url = urlparse("ws://" + self.prefixes)
            reactor.connectTCP(url.hostname, url.port, self)
            if isSync:
                self.syncSign.wait()
        except Exception as e:
            self.OnException(TrackException(code=ExceptionCode.Runtime, exception=e))

    def DisConnect(self):
        self.doStop()

    def OnConnectSuccess(self):
        reactor.callInThread(Client.OnConnectSuccess, self)

    def OnConnectFail(self):
        reactor.callInThread(Client.OnConnectFail, self)

    def OnDisConnect(self):
        reactor.callInThread(Client.OnDisConnect, self)


