from EtherealC.Core.BaseCore.BaseCore import BaseCore
from EtherealC.Core.Event import Event
from EtherealC.Core.Manager.AbstractType.AbstractTypeManager import AbstractTypeManager
from EtherealC.Core.Manager.Ioc.IocManager import IocManager
from EtherealC.Core.Model.TrackException import TrackException
from EtherealC.Core.Model.TrackLog import TrackLog


class MZCore(BaseCore):
    def __init__(self):
        BaseCore.__init__(self)
        self.iocManager = IocManager()
        self.types = AbstractTypeManager()
