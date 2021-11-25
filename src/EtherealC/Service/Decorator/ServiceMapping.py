class ServiceMapping:

    def __init__(self,mapping):
        self.mapping = mapping
        self.timeout = -1

    def __call__(self, func):
        func.ethereal_serviceMapping = self
        return func
