from EtherealC.Client.Abstract.ClientConfig import ClientConfig


class WebSocketClientConfig(ClientConfig):

    def __init__(self):
        super(WebSocketClientConfig, self).__init__()
        self.threadCount = 5
        self.connectTimeout = 6000
