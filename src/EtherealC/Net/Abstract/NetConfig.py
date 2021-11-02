from abc import ABC


class NetConfig(ABC):

    def __init__(self):
        self.maxThreadCount = 5

