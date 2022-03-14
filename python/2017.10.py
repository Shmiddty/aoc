import sys
from functools import partial
from operator import xor

from maths import product
from enum import flatten, rotate, chunk

class circular(list):
    def __iter__(self):
        i = 0
        while True:
            yield self[i]
            i = (i + 1) % len(self)

    def __getslice__(self, start, stop):
        gs = list.__getslice__
        unbounded = stop == sys.maxint
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

def step(ls, (s, n)):
    return circular(rotate(ls[:n][::-1] + ls[n:], (n + s) % len(ls)))

def skips(lens):
    return sum(map(sum, enumerate(lens)))

inp = sys.stdin.read().strip()

lens = map(int, inp.split(','))
string = circular(range(256))

part1 = rotate(reduce(step, enumerate(lens), string), -skips(lens))
print(product(part1[0:2]))

lens2 = flatten((map(ord, inp) + [17, 31, 73, 47, 23]) * 64, 1)
sparse = rotate(reduce(step, enumerate(lens2), string), -skips(lens2))
dense = map(partial(reduce, xor), chunk(sparse, 16))
part2 = ''.join('%02x'%v for v in dense)
print(part2)
