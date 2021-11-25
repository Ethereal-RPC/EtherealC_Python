import json

from EtherealC.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Utils import JsonTool


class AbstractTypeManager:

    def __init__(self):
        self.typesByType = dict()
        self.typesByName = dict()

    def add(self, **kwargs):
        rpc_type = AbstrackType()
        rpc_type.type = kwargs.get("type", None)
        rpc_type.name = kwargs.get("type_name", None)

        def deserializeFunc(_json):
            instance = rpc_type.type()
            di = None
            try:
                di = json.loads(_json)
            except:
                di = _json
            try:
                instance.__dict__ = di
            except:
                instance = di
            return instance

        def serializeFunc(obj):
            return json.dumps(obj, cls=JsonTool.JSONEncoder)

        rpc_type.deserialize = deserializeFunc
        rpc_type.serialize = serializeFunc
        if self.typesByName.get(rpc_type.name) is not None:
            raise TrackException(ExceptionCode.Core, "真实类中已包含" + rpc_type.name)
        self.typesByName[rpc_type.name] = rpc_type
        if self.typesByType.get(rpc_type.type) is None:
            self.typesByType[rpc_type.type] = rpc_type
