import sys
from functools import partial 
from operator import xor
from enum import circular, rotate, chunk, flatten

def step(ls, (s, n)):
    return circular(rotate(ls[:n][::-1] + ls[n:], (n + s) % len(ls)))

def skips(lens):
    return sum(map(sum, enumerate(lens)))

def hash(inp):
    string = circular(range(256))
    sugar = [17, 31, 73, 47, 23] # the elves add sugar to their knot-hashes 
    # except... they're programs. the narrative this year is unstable.
    lens = flatten((map(ord, inp) + sugar) * 64, 1)
    sparse = rotate(reduce(step, enumerate(lens), string), -skips(lens))
    dense = map(partial(reduce, xor), chunk(sparse, 16))
    return dense

def hashstr(inp): return ''.join('%02x'%v for v in hash(inp))
