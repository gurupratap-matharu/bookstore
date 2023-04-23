import time
from functools import wraps


def timeit(func):
    """
    Decorator function to stamp the runtime of any function or method.
    """

    @wraps(func)
    def inner_func(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        run = time.time() - start
        print(f"{func.__name__}: took {run:.2f} seconds!")

        return result

    return inner_func
