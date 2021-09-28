class ServerRequestModel:

    def __init__(self, **kwargs) -> None:
        self.Type = "ER-1.0-ServerRequest"
        self.MethodId = kwargs.get("method_id")
        self.Params = kwargs.get("params")
        self.Service = kwargs.get("service")
