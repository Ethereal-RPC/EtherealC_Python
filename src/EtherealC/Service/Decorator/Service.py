class Service:

    def __init__(self):
        pass

    def __call__(self, func):
        func.ethereal_service = self
        return func
