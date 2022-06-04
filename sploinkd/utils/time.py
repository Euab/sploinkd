from functools import wraps
from time import time


def timed(f):
    @wraps(f)
    def inner(*args, **kwargs):
        start = time()
        f(*args, **kwargs)
        end = time()
        delta = end - start

        print(f"\nProcess completed. time elapsed: {delta:.2f}s.")
    
    return inner
