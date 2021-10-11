from EtherealC.Core.Model.Error import Error


class ClientResponseModel:

    def __init__(self, **kwargs):
        self.Type: str = "ER-1.0-ClientResponse"
        self.Result: str = kwargs.get("result")
        self.Error: Error = kwargs.get("error")
        self.Id: str = kwargs.get("request_id")
        self.Service: str = kwargs.get("service")
