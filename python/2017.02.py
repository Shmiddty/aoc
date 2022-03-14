import sys
from enum import nth, permutations
from func import pipe, equals
from functools import partial

def minmax(ls):
    return (min(ls), max(ls))

def diff((a,b)):
    return b - a

def mod((a,b)):
    return a % b

def div((a,b)):
    return a / b

inp = [map(int, line.strip().split('\t')) for line in sys.stdin]
print(sum(map(pipe(minmax, diff), inp)))
print(sum(map(
    pipe(
        partial(permutations, r=2), 
        partial(filter, pipe(mod, equals(0))),
        nth(0),
        div
    ), 
    inp
)))
