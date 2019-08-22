[![Build Status](https://travis-ci.com/shouldsee/delay_and_cache.svg?branch=master)](https://travis-ci.com/shouldsee/delay_and_cache)

# delay_and_cache

A python extension that delays evaluation of function defaults and cache their outputs.

## Example 

```python
from delay_and_cache import delay_and_cache as _dac
from delay_and_cache import cacheThisFrame as _ctf
from delay_and_cache import CachedProxy
CachedProxy._DEBUG=1

@_dac
def start():
    print("[start]",1)
    return 1

@_dac
def middle( a=("start"), b="end"):
    _ctf()  ### evaluating all dependencies before proceed
    print("all values should be evaluated")
    return a() + b()  ### all arguments are callables

@_dac
def end():
    print("[end]",2)
    return 2

if __name__ == '__main__':
    print("[middle]",middle())
```

#[TBC]

