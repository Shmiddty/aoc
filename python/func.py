from functools import partial

prtl = partial
ppmap = prtl(prtl, map)

def call(a): return a()

def ffs(*A): return lambda *b: map(callWith(*b), A)
def fAb(A, b): return A(b)
def fBa(a, B): return B(a)
def fAB(A, B): return A(B())
def fABfab(A,B): return lambda a, b: (A(a), B(b))
def faBa(a, B): return a, B(a)
def I(a): return a
def swap(a, b): return b, a

def compose(a, b): #return lambda *x: a(b(*x))
    def COMPOSE(*x):
        return a(b(*x))
    return COMPOSE

def pipe(*fns): return reduce(compose, fns[::-1])

# There's an issue with this when args is a singular list
def curry(fn, *iargs, **iwds):
    def F(*args, **kwds):
        try: return fn(*args, **kwds)
        # Not strictly correct, but may function as intended
        except: return partial(F, *args, **kwds)
    return partial(F, *iargs, **iwds)

def wrap(x): return lambda *_: x

def spread(fn): return lambda ls: fn(*ls)

# these should maybe be moved to a boolean lib
def equals(val):
    return lambda Val: val == Val

def nequals(value): return pipe(equals(value), equals(False))

def fand(*fns):
    return lambda val: all(map(callWith(val), fns))

def less(val):
    return lambda Val: Val < val

def more(val):
    return lambda Val: Val > val

# these probably don't need to exist (unnecessary clutter)
def fall(*fns):
    return lambda val: all(map(callWith(val), fns))

def fany(*fns):
    return lambda val: any(map(callWith(val), fns))

# these should be moved to enum
# and also some of them already exist in itertools
def iterate(fn, v):
    while True:
        yield v
        v = fn(v)

def iterN(fn, n):
    return lambda v: map(lambda (_, b): b, zip(range(n + 1), iterate(fn, v)))

# basically pipe, but the values are accumulated
def over(*fns):
    def fn(v):
        out = [v]
        for f in fns:
            v = f(v)
            out.append(v)
        return out
    return fn

# itertools.repeat does a different thing
# don't confuse them
def repeat(fn, v):
    def F(n):
        cur = v
        while n > 0:
            n -= 1
            cur = fn(cur)
        return cur
    return F
    #return lambda n: reduce(lambda o,_: fn(o), range(n), v)

# I think the naming on this is problemating
# I keep forgetting that it takes a value at the outer level
def callWith(*val):
    return lambda f: f(*val)

def callwith(f): return lambda *val: f(*val)
def withval(*val): return lambda f: f(*val)
# this is kinda basically compose? but also not
def withresult(fnA): return lambda fnB: fnB(fnA())

def memo(fn, getKey = lambda *args:tuple(args)):
    cache = {}
    def F(*args):
        k = getKey(*args)
        if k not in cache: cache[k] = fn(*args)
        return cache[k]
    return F
