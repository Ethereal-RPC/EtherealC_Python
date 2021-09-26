import json
import multiprocessing
import sys
import threading
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse

from autobahn.twisted import WebSocketClientFactory

from Client.Abstract.Client import Client
from Client.WebSocket.WebSocketClientConfig import WebSocketClientConfig
from Client.WebSocket.WebSocketProtocol import WebSocketProtocol
from Core.Model.ClientRequestModel import ClientRequestModel
from Core.Model.TrackException import ExceptionCode, TrackException
from twisted.internet import reactor

from Core.Model.TrackLog import LogCode


class WebSocketClient(Client, WebSocketClientFactory):

    def __init__(self, net_name, service_name, prefixes, config: WebSocketClientConfig):
        self.prefixes = prefixes
        self.protocol = WebSocketProtocol
        self.handle = None
        self.connectSign = threading.Event()
        Client.__init__(self, net_name=net_name, service_name=service_name, config=config)
        WebSocketClientFactory.__init__(self, "ws://" + self.prefixes)

    def IsConnect(self):
        while self.handle is None:
            return False
        else:
            return self.handle.is_open

    def clientConnectionLost(self, *args, **kwargs):
        super(WebSocketClient, self).clientConnectionLost(args, kwargs)
        self.OnDisConnect()

    def clientConnectionFailed(self, *args, **kwargs):
        super(WebSocketClient, self).clientConnectionFailed(args, kwargs)
        self.OnDisConnect()

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
            self.connectSign.wait(self.config.connectTimeout)
        except Exception as e:
            self.OnException(TrackException(code=ExceptionCode.Runtime, exception=e))

    def DisConnect(self):
        try:
            self.sendClose()
        except Exception:
            pass

    def OnConnect(self):
        reactor.callInThread(Client.OnConnect, self)

    def OnDisConnect(self):
        reactor.callInThread(Client.OnDisConnect, self)


