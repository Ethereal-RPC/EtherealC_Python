import threading

from Core.Model.ClientResponseModel import ClientResponseModel


class ClientRequestModel:

    def __init__(self, **kwargs):
        self.Type = "ER-1.0-ClientRequest"
        self.MethodId = kwargs.get("method_id")
        self.Params = kwargs.get("params")
        self.Service = kwargs.get("service")
        self.Id: str = kwargs.get("request_id")
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
