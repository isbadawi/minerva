import functools

def cached(f):
    """
    Save the value returned by the wrapped function, so that subsequent
    calls don't perform the same computation.
    """
    value = [None]
    @functools.wraps(f)
    def wrapper():
        if value[0] is None:
            value[0] = f()
        return value[0]
    return wrapper
