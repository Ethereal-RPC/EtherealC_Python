class ServerRequestModel:

    def __init__(self, mapping,params,service) -> None:
        self.Type = "ER-1.0-ServerRequest"
        self.Mapping = mapping
        self.Params = params
        self.Service = service
