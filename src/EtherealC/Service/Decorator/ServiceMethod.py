class ServiceMethod:

    def __init__(self):
        self.timeout = -1

    def __call__(self, func):
        func.__doc__ = self
        return func
