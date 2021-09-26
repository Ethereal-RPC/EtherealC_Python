from Core.Model.AbstractTypes import AbstractTypes
from Core.Model.TrackException import TrackException
from Net.Abstract.Net import Net


class WebSocketNet(Net):
    def __init__(self,net_name):
        super().__init__(net_name=net_name)

    def Publish(self):
        if self.config.netNodeMode is True:
            pass
        else:
            try:
                for request in self.requests.values():
                    request.client.Start()
            except Exception as e:
                self.OnException(exception=TrackException(exception=e))
        return True
