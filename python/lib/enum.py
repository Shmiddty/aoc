def entuple(a): return (a,)

def enlist(a): return [a]

def concat(ls, val):
    return ls + (val if type(val) == list else [val])

def at(enum):
    return lambda i: enum[i]

def nth(n):
    return lambda enum: enum[n]

def within(enum):
    return lambda v: v in enum

def has(v):
    return lambda enum: v in enum

def head(ls): return ls[0]
def tail(ls): return ls[1:]
def decapitate(ls): return head(ls), tail(ls)

def mapgroup(ls, key=lambda en: en[0], val=lambda en: en[1:]):
    return [
        (K, [val(item) for item in ls if key(item) == K])
        for K in set(map(key, ls))
    ]

def permutations(enum, r):
    if len(enum) == 0: yield []
    elif r == 0: yield []
    elif r == 1: 
        for v in enum: yield [v]
    else:
        for (i, v) in enumerate(enum):
            for V in permutations(without(enum, i), r - 1):
                yield [v] + V

def combinations(enum, r):
    if len(enum) == 0: yield []
    elif r == 0: yield []
    elif r == 1: 
        for v in enum: yield [v]
    else:
        for (i, v) in enumerate(enum[0:-1]):
            for V in combinations(enum[i + 1:], r - 1):
                yield [v] + V

def take(n):
    return lambda e: list(map(nth(1), zip(range(n), e)))

# use builtin from itertools instead
def takeWhile(fn):
    def F(enum):
        out = []
        for v in enum:
            out.append(v)
            if not fn(v): break
        return out
    return F

def dropwhile(fn):
    def F(iterator):
        for v in iterator:
            if fn(v): continue
            yield v
    return F

# this is just zip. lel
def unzip(ls):
    return map(lambda i: map(nth(i), ls), range(len(ls[0])))

def izip(*iterators):
    while True:
        yield tuple(map(next, iterators))

def irange(start, stop = -1, step = 1):
    from itertools import takewhile, count
    if stop == -1: start, stop = 0, start
    return takewhile(lambda i: i < stop, count(start, step))

# workshop this naming.
# also, should it return a function that takes an enum instead?
def without(enum, i):
    return type(enum)(enum[0:i] + enum[i + 1:])

def discard(enum, i, n = 1):
    return type(enum)(enum[0:i] + enum[i + n:])

def replaceAt(enum, i, v):
    return type(enum)(enum[:i] + [v] + enum[i + 1:])

def divvy(ls, n):
    return [ls[i:i + n] for i in range(len(ls) - n + 1)]

def chunk(ls, n):
    return [ls[i:i + n] for i in range(0, len(ls) - n + 1, n)]

def aggregate(ls, key=lambda I:I, val=lambda I:I):
    vals = map(val, ls)
    return dict(map(lambda a: (key(a), vals.count(val(a))), ls))

def uniq(ls, key=lambda I:I):
    out = []
    hsh = {}
    for o in ls:
        v = key(o)
        if v not in hsh:
            out.append(o)
        hsh[v] = 1

    return out

def partition(ls, comparator = lambda a, b: a == b):
    cur = list(ls[0:1])
    out = [cur]
    for item in ls[1:]:
        prev = cur[-1]
        if not comparator(prev, item):
            cur = []
            out.append(cur)

        cur.append(item)
    
    return out

def flatten(ls, depth = 1):
    if depth < 0 or type(ls) != list: return [ls]
    return [item for enum in ls for item in flatten(enum, depth - 1)]

def repeats(s, n = 2):
    return filter(lambda ls: len(set(ls)) == 1, divvy(s, n))

def rotate(enum, n = 1):
    n = n % len(enum)
    return enum[n:] + enum[:n]

def swap(enum, a, b):
    mn, mx = min(a,b), max(a,b)
    return enum[:mn] + enum[mx:mx+1] + enum[mn+1:mx] + enum[mn:mn+1] + enum[mx+1:]

def swapval(enum, a, b):
    return swap(enum, enum.index(a), enum.index(b))

class circular(list):
    def __iter__(self):
        i = 0
        while True:
            yield self[i]
            i = (i + 1) % len(self)

    def __getslice__(self, start, stop):
        from sys import maxint # python is kinda magical with these scoped imports

        gs = list.__getslice__
        unbounded = stop == maxint
        L = len(self)
        N = stop - start
        S = start % L
        P = S + N #if not unbounded else sys.maxint

        if start >= L and unbounded: return []
        if P > L and not unbounded:
            return gs(self, S, L) + gs(self, 0, P % L)

        return gs(self, S, P)

    def __getitem__(self, i):
        return list.__getitem__(self, i % len(self))
