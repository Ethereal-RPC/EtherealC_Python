from EtherealC.Core.Model.Error import Error


class ClientResponseModel:

    def __init__(self, result=None,error=None,id=None):
        self.Type: str = "ER-1.0-ClientResponse"
        self.Result: str = result
        self.Error: Error = error
        self.Id: str = id
