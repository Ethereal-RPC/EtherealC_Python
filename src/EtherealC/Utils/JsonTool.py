import json
import threading
from typing import Any

from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.Error import Error


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        d = {}
        d.update(obj.__dict__)
        return d


class JSONClientResponseModel(json.JSONEncoder):
    def default(self, obj: ClientResponseModel) -> Any:
        if isinstance(obj, Error):
            obj.Code = obj.Code.service_name
            return obj.__dict__


class JSONClientRequestModel(json.JSONEncoder):
    def default(self, obj: ClientRequestModel) -> Any:
        if isinstance(obj, threading.Event):
            return None

