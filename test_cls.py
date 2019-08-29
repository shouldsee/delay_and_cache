from delay_and_cache import delay_and_cache as _dac
from delay_and_cache import cacheThisFrame as _ctf
from delay_and_cache import CachedProxy
from delay_and_cache import StaticClass
CachedProxy._DEBUG=1

class a_cls(object):
    __metaclass__ = StaticClass
    A = "A"
    B = "B"
    @_dac
    def start():
        print("[start]",1)
        return 1

    @_dac
    def middle( a=("start"), b="end"):
        _ctf()  ### evaluating all dependencies before proceed
        print("[middle] all values should be evaluated")
        return a() + b()  ### all arguments are callables

    @_dac
    def end():
        print("[end]",2)
        return 2
    @_dac
    def findA(A="A"):
        A()
        pass
    @_dac
    def findB(_B = "_B"):
        _B()
        pass
    
    @_dac
    def findC(C = "C"):
        C()
        pass
    
C = "globalC"

import unittest
unittest.TestCase.assertRaises

class test(unittest.TestCase):
    def runTest(self):
        a_cls.middle()
        a_cls.findA()
        self.assertRaises( AssertionError, a_cls.findB )
#         self.assertRaises(AssertionError, a_cls.findC )
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test())