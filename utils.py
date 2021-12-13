from functools import wraps
import time

def delay(t: int=1):
    def decorator_delay(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            time.sleep(t)
            return f(*args, **kwargs)
        return wrapper
    return decorator_delay
