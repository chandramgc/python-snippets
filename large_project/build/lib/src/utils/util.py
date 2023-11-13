import time

def duration(method):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{method.__name__} took {duration:.4f} seconds to execute")
        return result
    return wrapper