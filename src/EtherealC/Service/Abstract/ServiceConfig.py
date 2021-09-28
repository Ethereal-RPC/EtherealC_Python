from abc import ABC

from EtherealC.Core.Model.AbstractTypes import AbstractTypes


class ServiceConfig(ABC):

    def __init__(self, _type: AbstractTypes):
        self.types: AbstractTypes = _type
