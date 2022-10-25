# pyrsc: triggers task when enough resources are available
[![PyPI Latest Release](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.org/project/diclass/)

## What is it?

**pyrsc** Sometime we need to run a job or function in Python when enough resources are available. For example, you are running several machine learning models to train in parallel. But you want to avoid running them all at once becuase they utilize cpu and memory resources a lot.

## Example


```python
from pyrsc import watch
from joblib import delayed, Parallel
```

I am trying to run several foo function at once, but I need them to run when at least 16 cores (`n_cores`) are utilized less than 5% (`max_perc`), if not recheck after 0.001 second (`sleep_interval`). In total if it fails to after 10 attempts (`max_attempts`), it has to raise an exception.


```python
@watch(max_attempts=10, cpu=5, n_cores=16, sleep_interval=0.001)
def foo(x):
    print(x)
    
jobs = [delayed(foo)(i) for i in range(10)]
Parallel(n_jobs=32)(jobs);
```

    not enough resource is available to submit the job. Waiting for 0.001 seconds
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    0
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    1
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    2
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    3
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    4
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    5
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    6
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    not enough resource is available to submit the job. Waiting for 0.001 secondsnot enough resource is available to submit the job. Waiting for 0.001 seconds
    
    7
    8
    not enough resource is available to submit the job. Waiting for 0.001 seconds
    9


Lets see what if we set `max_perc=100`


```python
@watch(max_attempts=10, cpu=50, n_cores=1, sleep_interval=0.001)
def foo(x):
    print(x)
    
jobs = [delayed(foo)(i) for i in range(10)]
Parallel(n_jobs=32)(jobs);
```

    0
    4
    2
    3
    1
    5
    6
    7
    8
    9


In future release I will add the ability to manage also memory and virtual memory. Also total cpu usage will be implemented to avoid a job to run once resource requirments are not available.


```python

```
