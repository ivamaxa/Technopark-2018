import time
from functools import wraps


def profile(func):
    if isinstance(func, type):
        for met in dir(func):
            if not met.startswith('__') or met == '__init__':
                attr = getattr(input, met)
                setattr(func, met, profile(attr))

        return func
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(func.__name__ + ' started')
            start = time.time()
            result = func(*args, **kwargs)
            stop = time.time()
            print(func.__name__ + ' finished in {0}s'.format(round(stop - start, 3)))
            return result

        return wrapper


