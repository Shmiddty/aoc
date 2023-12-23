import sys
import re
from functools import reduce
from func import pipe, curry, juxt
from enumtools import nth
from maths import add, product

def split(s):
    return lambda st: st.split(s)

def lmap(fn, it):
    return list(map(fn, it))

def strip(s):
    return s.strip()

def dmerge(ls):
    d = {'red':[], 'green':[], 'blue':[]}
    for k, v in ls:
        d[k].append(v)
    return d

def check(red, green, blue):
    return lambda d: d['red'] <= red and d['green'] <= green and d['blue'] <= blue

def dmap(fn, d):
    return { k:fn(v) for k,v in d.items() }

pipe(
    curry(map, pipe(
        split(':'),
        nth(1),
        pipe(
            curry(re.findall, r"[^,;]+"),
            curry(lmap, pipe(
                strip, 
                split(' '), 
                lambda ls: (ls[1], int(ls[0]))
            )),
            dmerge,
            curry(dmap, max)
        ),
    )),
    enumerate,
    list,
    juxt(
        pipe(
            curry(filter, pipe(nth(1), check(12,13,14))),
            curry(map, pipe(nth(0), curry(add, 1))),
            curry(reduce, add)
        ),
        pipe(
            curry(map, pipe(
                nth(1),
                lambda d: d.values(),
                product
            )),
            curry(reduce, add)
        )
    ),
    list,
    print
)(sys.stdin)

