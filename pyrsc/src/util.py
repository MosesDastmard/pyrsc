import psutil
import time

class Watch:
    def __init__(self, cpu:float=0, n_cores:int=0, memory:float=0.0, sleep_interval:float=0.01, max_attempts:int=0):
        self.cpu = cpu
        self.n_cores = n_cores
        self.sleep_interval = sleep_interval
        self.memory = memory
        self.max_attempts = max_attempts
        
    def __trigger(self):
        cpu_percs = psutil.cpu_percent(percpu=True)
        memory_available = psutil.virtual_memory()[1]/1024**2
        if (sum([(100 - perc) > self.cpu for perc in cpu_percs]) >= self.n_cores) & (memory_available > self.memory):
            return True
        return False
    
    def __enter__(self):
        attempts = 0
        while (attempts <= self.max_attempts) or (self.max_attempts == 0):
            if self.__trigger():
                return self
            else:
                print(f'not enough resource is available to submit the job. Waiting for {self.sleep_interval} seconds')
                attempts += 1
                time.sleep(self.sleep_interval)
        raise Exception("attempts exceeds max_attempts")

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass
    
def watch(cpu:float=0.0, n_cores:int=0, memory:float=0.0, sleep_interval:float=0.01, max_attempts:int=0):
    def inner(func):
        def wrapper(*args, **kwargs):
            with Watch(cpu=cpu, n_cores=n_cores, memory=memory, sleep_interval=sleep_interval, max_attempts=max_attempts) as watcher:
                return func(*args, **kwargs)
        return wrapper
    return inner