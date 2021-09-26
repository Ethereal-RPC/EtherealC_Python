from Net.NetNodeClient.Model.NetNode import NetNode
from Request.Decorator.Request import Request


class ServerNetNodeRequest:
    @Request()
    def GetNetNode(self, servicename: str) -> NetNode:
        pass
