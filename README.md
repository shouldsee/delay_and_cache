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


'''
[eval]<CachedProxy at 0x7f5ec5ae6ad0 for <function step6 at 0x7f5ec5aebb90>>
[eval]<CachedProxy at 0x7f5ec5ae6550 for <function start at 0x7f5ec5aeb1b8>>
[eval]<CachedProxy at 0x7f5ec5ae6d90 for <function end at 0x7f5ec5aeb410>>
Middle
[acce]<CachedProxy at 0x7f5ec5ae6550 for <function start at 0x7f5ec5aeb1b8>>
[acce]<CachedProxy at 0x7f5ec5ae6d90 for <function end at 0x7f5ec5aeb410>>
(3,)
[eval]<CachedProxy at 0x7f5ec5ae6550 for <function middle at 0x7f5ec5aebd70>>
[eval]<CachedProxy at 0x7f5ec5ae6fd0 for <function start at 0x7f5ec5aebc80>>
('[start]', 1)
[eval]<CachedProxy at 0x7f5ec5af60d0 for <function end at 0x7f5ec5aebde8>>
('[end]', 2)
[middle] all values should be evaluated
[acce]<CachedProxy at 0x7f5ec5ae6fd0 for <function start at 0x7f5ec5aebc80>>
[acce]<CachedProxy at 0x7f5ec5af60d0 for <function end at 0x7f5ec5aebde8>>
('[middle]', 3)
'''
```

#[TBC]

