def Service(**top_args):
    paramters = top_args.get("paramters", None)
    timeout = top_args.get("timeout", -1)

    def getFunc(func):
        def Func(*args, **kwargs):
            return func(*args, **kwargs)

        annotation = ServiceAnnotation()
        annotation.paramters = paramters
        annotation.timeout = timeout
        Func.__doc__ = annotation
        Func.__annotations__ = func.__annotations__
        Func.__name__ = func.__name__
        return Func

    return getFunc


class ServiceAnnotation:
    timeout = -1
    paramters = None
