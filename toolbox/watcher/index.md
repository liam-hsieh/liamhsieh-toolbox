# toolbox.watcher  
*module*, watcher is created to trace and record program performance and keep the history.  

## toolbox.watcher.timeit
*class*, put the decorator `timeit` on class method you want to check the run time and then check the property watcher


```python
import toolbox.watcher.timeit as timeit

class test1:
    def __init__(self):
        pass
    @timeit
    def test_run(self):
        fake_data_gen = (x for x in range(100000))
        j=0
        for i in fake_data_gen:
            j+=i    
        return j

t1 = test1()
print(f'run time in sec: {t1.test_run()}')
print(t1.watcher)
```

```noghighlight
    run time in sec: 4999950000
    {'run_time': {'code': 'test_run', 'start_time': datetime.datetime(2022, 8, 2, 0, 58, 36, 688376), 'end_time': datetime.datetime(2022, 8, 2, 0, 58, 36, 698302), 'run time(sec)': 0.009926}}
```

## toolbox.watcher.get_obj_size
*function*, return the size of given object

```nohighlight
Args:
    obj (object): any Python object

Returns:
    str: size of the object
    
```

```python
from toolbox.watcher import get_obj_size
foo = lambda x:(x+1)^200000
a = foo(100)
get_obj_size(a)
```

```nohighlight
'32.000 bytes'
```