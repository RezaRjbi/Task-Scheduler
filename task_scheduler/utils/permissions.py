def get_req_and_kwarg(args: tuple, kwargs: dict, kw: str):
    """
    get the request object from pos-arguments and kw from keyword-arguments from decorated functions.
    if kwargs not provided just the request object will be returned.
    we need this values to set different permissions for different users
    """
    if not kw:
        return args[1], None
    return args[1], kwargs.get(kw)

