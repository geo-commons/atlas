from functools import wraps


def request_cache(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request is None:
            return func(request, *args, **kwargs)

        cache = request.__dict__.setdefault('_request_cache', {})
        key = (func, args, frozenset(kwargs.items()))

        if key not in cache:
            cache[key] = func(request, *args, **kwargs)

        return cache[key]

    return wrapper
