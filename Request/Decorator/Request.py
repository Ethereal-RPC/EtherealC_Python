def Request(**top_args):
    paramters = top_args.get("paramters", None)
    timeout = top_args.get("timeout", None)

    def getFunc(func):
        def Func(*args, **kwargs):
            func(*args, **kwargs)

        annotation = RequestAnnotation()
        annotation.paramters = paramters
        Func.__doc__ = annotation
        Func.__name__ = func.__name__
        Func.__annotations__ = func.__annotations__
        return Func

    return getFunc


class RequestAnnotation:
    paramters = None
    timeout = None
