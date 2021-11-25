import threading

from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel


class ClientRequestModel:

    def __init__(self, mapping = None,params=dict(),id=None):
        self.Type = "ER-1.0-ClientRequest"
        self.Mapping = mapping
        self.Params = params
        self.Id: str = id
        self.Result = None
        self.Sign = threading.Event()

    def Set(self, result: ClientResponseModel):
        self.Result = result
        self.Sign.set()

    def Get(self, timeout):
        if self.Result is None:
            if timeout == -1:
                self.Sign.wait()
            else:
                self.Sign.wait(timeout)
        return self.Result
