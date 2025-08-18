import time
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Tempo di esecuzione di {func.__name__}: {end_time - start_time} secondi")
        return result
    return wrappe