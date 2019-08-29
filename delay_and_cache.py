import functools
import types
import itertools
import inspect

import json
def dppJson(d,**kw):
    '''
    dirtly serialise and pretty print a dictionary
    '''
    s = json.dumps(d,indent=4, sort_keys=True,defaut=repr,**kw)
    return s

class StaticClass(type):
    '''
    Force all function attributess to be staticmethod()s
    '''
    _DEBUG = 0
    def __new__(meta, cls_name, cls_bases, cls_attrs):
#         lcs = {}
        for k,v in cls_attrs.iteritems():
            if inspect.isfunction(v):
                cls_attrs[k] = staticmethod(v)
            elif inspect.isclass(v):
                pass
            elif callable(v):
                pass
            elif inspect.ismethoddescriptor(v):
                assert isinstance(v,staticmethod),(k,type(v),)
            else:
                ### collect con
#                 lcs[k] = v
                pass

            if meta._DEBUG:
                print (inspect.ismethod(v),
                       inspect.isclass(v),
                       inspect.isfunction(v),
                       inspect.ismethoddescriptor(v),
                       callable(v),
                       k,
                       v)

        cls = type.__new__(meta, cls_name, cls_bases, cls_attrs)
        return cls
    
def func__currName():
    return inspect.currentframe().f_back.f_code.co_name    
_fkey = func__currName


def rgetattr_dft(obj,attr,dft):
    _this_func = rgetattr_dft
    sp = attr.split('.',1)
    if len(sp)==1:
        l,r = sp[0],''
    else:
        l,r = sp
        
    obj = getattr(obj, l, dft)
    if r:
        obj = _this_func(obj, r, dft)
    return obj

def frame__default(frame=None):
# def frame__parent(frame=None):
    if frame is None:
        frame = inspect.currentframe().f_back.f_back ####parent of caller by default
    else:
        pass    
    return frame

def name__lookup(name,frame=None,level=1, 
#                  getter="dict"
                ):
    '''
    if level==0, get the calling frame
    if level > 0, walk back <level> levels from the calling frame
    '''
    if frame is None:
        frame = inspect.currentframe()
    errMsg = ("Unable to lookup name {name} within level {level}".format(**locals()))
    
    i = 0
    while i != level:
        i+=1;
#     for i in range(level):
        if name in frame.f_locals:
            val = frame.f_locals[name]
            del frame
            return val
        
        frame = frame.f_back
        assert frame is not None,errMsg
        
    del frame        
    assert 0,errMsg

def func__castingDefaults(casters):
    '''
    casting Defaults of the function
    '''
    if isinstance(casters,type):
        casters = itertools.cycle([casters])
    def dec(f):
        _defaults = ()
        for i,(caster,val) in enumerate(
            zip(casters, f.__defaults__ or [] )
        ):
            _defaults  += (caster(val),)
        g = types.FunctionType(f.__code__, 
                               f.__globals__, 
                               f.__name__, 
                               _defaults,
#                                f.__defaults__, 
                               f.__closure__)    
        return functools.wraps(f)(g)
    return dec


def func__castDelayedParam(f,frame=None):
    frame = frame__default(frame)
    class cls_dpar(DelayParam):
        _frame = frame
    return func__castingDefaults(cls_dpar)(f)
_fcdpar = func__castDelayedParam

if __name__ == '__main__':
    @func__castingDefaults([int])
    def f(x=0.1):
        '''
        A
        '''
        return x
    assert f() ==0

    @func__castingDefaults(int)
    def f(x=0.1):
        '''
        A
        '''
        return x
    assert f() ==0

        
class CallableProxy(object):
    def __init__(self,clb):
        assert callable(clb)
        self._callable = clb
        
    @staticmethod
    def __prj__(v):
        '''
        Test for bytecode equvalence
        '''
        return ( 
            rgetattr_dft(v,"__code__.co_code",None),
            rgetattr_dft(v,"__code__.co_consts",None),
               )

    def __eq__(self,other):
        return self.__prj__(self) == self.__prj__(other)
#         return self._callable == getattr(other,"_callable",None)
    
    def __call__(self, *a, **kw):
        return self._callable(*a,**kw)
    
    def __getattr__(self, k):
        return getattr(self._callable, k)
    
    def __repr__(self):
        return "<%s at 0x%x for %r>"%( 
            self.__class__.__name__,
            id(self),
            self._callable)
    
    

class DelayParam(CallableProxy):
    _frame = None
    def __init__(self, name,frame=None):
        cls = self.__class__
        self._name  = name
        self._frame = frame__default() if cls._frame is None else cls._frame
        def clb(self=self, *a,**kw):
            x = name__lookup(
            name = self._name,
            frame= self._frame,
            level= -1)            
            if callable(x):
                return x(*a,**kw)
            else:
                return x
        self._callable = clb
        
#         self._callable = lambda *a,**kw: name__lookup(
#             name = self._name,
#             frame= self._frame,
#             level= -1)(*a,**kw)
    @staticmethod
    def __prj__(self):
        '''
        Test for registry equivalence
        '''
        return (
            getattr(self,"_name",None),
            rgetattr_dft(self,"_frame.f_code.co_name",None),
            rgetattr_dft(self,"_frame.f_code.co_filename",None),
        )
    def __eq__(self,other):
        return self.__prj__(self) == self.__prj__(other)
        
class CachedProxy(CallableProxy):
    '''
    Same as CallableProxy() but overrides __call__ to ensure
    single evaulation
    '''
    
    _INIT = object()
    _DEBUG = 0
    def __init__(self, clb):
        self._callable = clb
        self._value = self._INIT
        
    def __call__(self,*a,**kw):
        if self._value is self._INIT:
            if self._DEBUG:
                print ('[eval]%r'%self)
            self._value = self._callable(*a,**kw)
        else:
            if self._DEBUG:
                print ('[acce]%r'%self)
            pass
        return self._value
    



def UnrollProxy(dp):
    if isinstance(dp, CallableProxy):
        return UnrollProxy(dp())
    else:
#         print type(dp)
        return dp

def func__cachedCastDelayedParam(f,frame=None):
    f = func__castDelayedParam(f, frame__default(frame))
    f = CachedProxy(f)
    return f

delay_and_cache = _fccdp = func__cachedCastDelayedParam

def cacheThisFrame():
    d =  frame__default().f_locals
    return [x() if callable(x) else x for x in d.values() ]

_ctf = cacheThisFrame
_cpx = CachedProxy
_upx = UnrollProxy
_dpar = DelayParam


if __name__ == '__main__':
    @_cpx
    def start():
        return 1


    @_cpx
    def step( a=_dpar("start"), b=_dpar("end")):
        a = _upx(a)
        b = _upx(b)

        return a + b

    @_cpx
    @_fcdpar
    def step2( a=("start"), b="end"):
        a = _upx(a)
        b = _upx(b)
        return a + b


    @_fccdp
    def step3( a=("start"), b="end"):
        a = _upx(a)
        b = _upx(b)
        return a + b

    @_fcdpar
    @_cpx
    def step4( a=("start"), b="end"):
        a = _upx(a)
        b = _upx(b)
        return a - b


    @_cpx
    @_fcdpar
    def step5( a=("start"), b="end"):
        return a() + b()


    @_fccdp
    def step6( a=("start"), b="end"):
        _ctf()
        print ("[Middle]",)
        return a() + b()

    @_cpx
    def end():
        return 2

    CachedProxy._DEBUG = 1
#     class CachedProxy(CallableProxy):
    assert step2 == step == step3
    assert step != step4
    assert step2.__defaults__ == step.__defaults__ == step3.__defaults__ \
        == step4.__defaults__ 
    
    print (step6(),)
    CachedProxy._DEBUG = 0
    
