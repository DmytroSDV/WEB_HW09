from functools import wraps
import time

def async_time(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        start = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            print(time.perf_counter() - start)

    return wrapped


def sync_time(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(time.perf_counter() - start)
    return wrapped
    

