import sys
from functools import partial as curry

from func import iterate, pipe, equals
from string import digits
from enum import take, izip, dropwhile

A = 16807
B = 48271
R = 2147483647

a0, b0 = [digits(line)[0] for line in sys.stdin]

aI = iterate(lambda v: v * A % R, a0)
bI = iterate(lambda v: v * B % R, b0)

def toInt16(v): return (2**16-1) & v
def diff((a,b)): return b-a

# very slow
# too many list items? probably need to do it stepwise
#pairs = take(40*10**6)(izip(aI, bI))
#matching = filter(
#    pipe(
#        curry(map, toInt16), 
#        diff, 
#        equals(0)
#    ), 
#    pairs
#)
#
#print(len(matching))

# still pretty slow, but it finishes
def countMatches(itr, n = 5):
    tot = 0
    while n > 0:
        n -= 1
        pair = map(toInt16, next(itr))
        tot += diff(pair) == 0

    return tot

# part1
#print(countMatches(izip(aI, bI), 40*10**6))

Ar = 4
Br = 8

a2I = dropwhile(lambda v: v % Ar)(aI)
b2I = dropwhile(lambda v: v % Br)(bI)

# part2
print(countMatches(izip(a2I, b2I), 5*10**6))
