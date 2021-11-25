import threading

from EtherealC.Client.WebSocket.WebSocketClient import WebSocketClient
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Net.Abstract.Net import Net
from EtherealC.Net.WebSocket.WebSocketNetConfig import WebSocketNetConfig


class WebSocketNet(Net):
    def __init__(self, name):
        super().__init__(name=name)
        self.config = WebSocketNetConfig()
        self.connectSign = threading.Event()

    def Publish(self):
        def reactorStart():
            from twisted.internet import reactor
            if not reactor.running:
                reactor.suggestThreadPoolSize(10)
                reactor.run(False)

        threading.Thread(target=reactorStart).start()
        return True
