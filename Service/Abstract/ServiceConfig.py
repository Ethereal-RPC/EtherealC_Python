from abc import ABC

from Core.Model.AbstractTypes import AbstractTypes
from Service.Abstract import Service


class ServiceConfig(ABC):

    def __init__(self, _type: AbstractTypes):
        self.types: AbstractTypes = _type
