import re

from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode

pattern = re.compile('\w+')


class EventSender:
    def __init__(self, method):
        self.function = method
        self.method = None
        self.instance = None
        self.paramsMapping = dict()

    def __call__(self, func):
        result = pattern.findall(self.function)
        if result.__len__() < 2 or result.__len__() % 2 != 0:
            raise TrackException(ExceptionCode.Runtime, "{0}方法的{1}事件定义不合法".format(func.__name__, self.method))
        self.instance = result[0]
        self.method = result[1]
        for i in range(0, result.__len__())[::2]:
            self.paramsMapping[result[i]] = result[i + 1]
            i = i + 1
