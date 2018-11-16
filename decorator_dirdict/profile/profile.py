import time
from functools import wraps
from types import FunctionType


def profile(func):

    if isinstance(func, type):
        for met in dir(func):
          if isinstance(met, FunctionType) or met == '__init__':
                attr = getattr(func, met)
                setattr(func, met, profile(attr))
        return func
    return output(func)


def output(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(func.__qualname__ + ' started')
            start = time.time()
            result = func(*args, **kwargs)
            stop = time.time()
            print(func.__qualname__ + ' finished in {0}s'.format(round(stop - start, 3)))
            return result

        return wrapper


