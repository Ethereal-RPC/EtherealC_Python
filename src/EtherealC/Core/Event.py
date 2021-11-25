class Event:
    def __init__(self):
        self.__listeners__: list = list()

    def Register(self, delegate):
        if delegate not in self.__listeners__:
            self.__listeners__.append(delegate)

    def unRegister(self, delegate):
        self.__listeners__.remove(delegate)

    def onEvent(self, **params):
        for delegate in self.__listeners__:
            delegate(**params)
