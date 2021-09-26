from Core.Model.AbstractTypes import AbstractTypes


class RequestConfig:

    def __init__(self, config_type: AbstractTypes):
        self.types = config_type
        self.timeout = -1
