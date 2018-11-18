import time
from functools import wraps
from types import FunctionType

def profile(func):
    if isinstance(func, type):
        for met in func.__dict__.items():
            if isinstance(met[1], FunctionType):
                attr = getattr(func, met[0])
                #print(attr)
                class_name  =func.__name__
                setattr(func, met[0], output(attr, class_name))
        return func
    return output(func)


def output(func, class_name=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        name = func.__name__
        #print(name)
        if class_name is not None:
            name = "{}.{}".format(class_name, name)
        print(name + ' started')
        result = func(*args, **kwargs)
        stop = time.time()
        print(name + "finished in {0}s".format(round(stop-start, 3)))
        return result

    return wrapper




@profile
class Bar:
    def __init__(self):
        pass
Bar()
