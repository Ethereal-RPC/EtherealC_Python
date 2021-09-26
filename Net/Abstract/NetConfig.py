from abc import ABC

from Service.Abstract.Service import Service


class NetConfig(ABC):

    def __init__(self):
        self.netNodeMode = False
        self.netNodeIps = None
        self.netNodeHeartbeatCycle = 60000

