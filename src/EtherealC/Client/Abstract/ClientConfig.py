import json
from abc import ABC

from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.ServerRequestModel import ServerRequestModel
from EtherealC.Utils.JsonTool import JSONClientRequestModel


class ClientConfig(ABC):

    def __init__(self):
        self.auto_manage_token = True
        self.encode = "utf-8"

        def clientRequestModelSerializeFunc(obj: ClientRequestModel) -> str:
            return json.dumps(obj.__dict__, ensure_ascii=False, cls=JSONClientRequestModel)

        self.ClientRequestModelSerialize = clientRequestModelSerializeFunc

        def serverRequestModelDeserializeFunc(_json: str) -> ServerRequestModel:
            instance = ServerRequestModel()
            di = json.loads(_json)
            try:
                instance.__dict__ = di
            except:
                instance = None
            return instance

        self.ServerRequestModelDeserialize = serverRequestModelDeserializeFunc

        def clientResponseModelDeserializeFunc(_json: str) -> ClientResponseModel:
            instance = ClientResponseModel()
            di = json.loads(_json)
            try:
                instance.__dict__ = di
            except:
                instance = None
            return instance

        self.ClientResponseModelDeserialize = clientResponseModelDeserializeFunc
