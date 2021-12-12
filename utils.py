from functools import wraps
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def delay(t: int=1):
    def decorator_delay(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            time.sleep(t)
            return f(*args, **kwargs)
        return wrapper
    return decorator_delay
