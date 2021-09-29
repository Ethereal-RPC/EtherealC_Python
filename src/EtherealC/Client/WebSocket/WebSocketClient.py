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

    def __init__(self, net_name, service_name, prefixes, config: WebSocketClientConfig):
        if config is None:
            config = WebSocketClientConfig()
        self.prefixes = prefixes
        self.protocol = WebSocketProtocol
        self.handle = None
        self.connectSign = threading.Event()
        WebSocketClientFactory.__init__(self, "ws://" + self.prefixes)
        Client.__init__(self, net_name=net_name, service_name=service_name, config=config)

    def IsConnect(self):
        while self.handle is None:
            return False
        else:
            return self.handle.is_open

    def clientConnectionLost(self, *args, **kwargs):
        super(WebSocketClient, self).clientConnectionLost(args, kwargs)
        self.OnDisConnectFail()

    def clientConnectionFailed(self, *args, **kwargs):
        super(WebSocketClient, self).clientConnectionFailed(args, kwargs)
        self.OnDisConnectFail()

    def SendClientRequestModel(self, request: ClientRequestModel):
        request_body = self.config.ClientRequestModelSerialize(request)
        self.handle.sendMessage(request_body.encode(self.config.encode))
        return True

    def Connect(self):
        try:
            from twisted.python import log
            log.startLogging(sys.stdout)
            url = urlparse("ws://" + self.prefixes)
            reactor.connectTCP(url.hostname, url.port, self)
            if not reactor.running:
                reactor.run()
            self.connectSign.wait(self.config.connectTimeout/1000)
            if self.handle is None:
                self.OnDisConnectFail()
        except Exception as e:
            self.OnDisConnectFail()
            self.OnException(TrackException(code=ExceptionCode.Runtime, exception=e))

    def DisConnect(self):
        try:
            self.sendClose()
        except Exception:
            pass

    def OnConnectSuccess(self):
        reactor.callInThread(Client.OnConnectSuccess, self)

    def OnDisConnectFail(self):
        reactor.callInThread(Client.OnDisConnectFail, self)

    def OnDisConnect(self):
        reactor.callInThread(Client.OnDisConnect, self)


