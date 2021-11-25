import sys

from EtherealC.Core.Manager.AbstractType.AbstractType import AbstrackType
from EtherealC.Core.Manager.Event.Model.EventContext import EventContext
from EtherealC.Core.Model.ClientRequestModel import ClientRequestModel
from EtherealC.Core.Model.ClientResponseModel import ClientResponseModel
from EtherealC.Core.Model.TrackException import TrackException, ExceptionCode
from EtherealC.Request.Abstract.Request import Request


def getInvoke(func):
    def invoke(self:Request,*args,**kwargs):
        from EtherealC.Request.Decorator import InvokeTypeFlags
        from EtherealC.Request.Decorator.RequestMapping import RequestMapping
        requestMapping: RequestMapping = func.ethereal_requestMapping
        requestModel = ClientRequestModel(mapping=requestMapping.mapping)
        localResult = None
        remoteResult = None
        methodResult = None
        eventContext = EventContext()
        eventContext.method = func
        if hasattr(func,"ethereal_beforeEvent"):
            self.iocManager.InvokeEvent(func.ethereal_beforeEvent,kwargs,eventContext)
        keys = list(func.__annotations__.keys())
        for i in range(args.__len__()):
            kwargs[keys[i]] = args[i]
        if requestMapping.invokeType & InvokeTypeFlags.Local != 0:
            try:
                localResult = func(self,**kwargs)
            except Exception as e:
                if hasattr(func, "ethereal_exceptionEvent"):
                    eventContext.exception = e
                    self.iocManager.InvokeEvent(func.ethereal_exceptionEvent, kwargs, eventContext)
                    if func.ethereal_exceptionEvent.isThrow:
                        raise e
                else:
                    raise e
        if hasattr(func, "ethereal_afterEvent"):
            eventContext.result = localResult
            self.iocManager.InvokeEvent(func.ethereal_afterEvent,kwargs,eventContext)
        if requestMapping.invokeType & InvokeTypeFlags.Remote != 0:
            for v,k in func.__annotations__.items():
                if v == "return":
                    continue
                requestModel.Params[v] = k.serialize(kwargs[v])
            if func.__annotations__["return"] is None:
                self.client.SendClientRequestModel(requestModel)
            else:
                requestModel.Id = str(self.random.randint(0, sys.maxsize))
                while self.task.get(requestModel.Id) is not None:
                    requestModel.Id = str(self.random.randint(0, sys.maxsize))
                self.task[requestModel.Id] = requestModel
                try:
                    timeout = requestMapping.timeout
                    if timeout is not None:
                        timeout = self.config.timeout
                    if self.client.SendClientRequestModel(requestModel):
                        response: ClientResponseModel = requestModel.Get(timeout)
                        if response is not None:
                            if response.Error is not None:
                                if hasattr(func, "ethereal_failEvent"):
                                    eventContext.error = response.Error
                                    self.iocManager.InvokeEvent(func.ethereal_failEvent, kwargs, eventContext)
                                    if func.ethereal_failEvent.isThrow:
                                        raise TrackException(code=ExceptionCode.Runtime,
                                                             message="来自服务端的报错消息：\n" + response.Error.Message)
                                else:
                                    raise TrackException(code=ExceptionCode.Runtime,
                                                         message="来自服务端的报错消息：\n" + response.Error.Message)
                            else:
                                return_type = func.__annotations__.get("return")
                                remoteResult = return_type.deserialize(response.Result)
                                if hasattr(func, "ethereal_successEvent"):
                                    eventContext.result = remoteResult
                                    self.iocManager.InvokeEvent(func.ethereal_successEvent, kwargs, eventContext)
                        elif hasattr(func, "ethereal_timeoutEvent"):
                            self.iocManager.InvokeEvent(func.ethereal_timeoutEvent, kwargs, eventContext)
                finally:
                    del self.task[requestModel.Id]
        if (requestMapping.invokeType & InvokeTypeFlags.ReturnRemote) != 0:
            methodResult = remoteResult
        elif (requestMapping.invokeType & InvokeTypeFlags.ReturnLocal) != 0:
            methodResult = localResult
        return methodResult
    invoke.__dict__ = func.__dict__
    invoke.__name__ = func.__name__
    invoke.__annotations__ = func.__annotations__
    return invoke
