import sys

from func import iterate
from enum import takeWhile
from maths import product

# [(depth, range), ...]
inp = [map(int, line.split(': ')) for line in sys.stdin]

# not actually the position
def pos(t0): return lambda (d, r): (t0 + d) % (2 * r - 2)
def isCaught(t0): return lambda (d, r): pos(t0)((d,r)) == 0

caught = filter(isCaught(0), inp)

# part 1
print(sum(map(lambda (d, r): d * r, caught)))

# part 2
# this is too slow
steps = takeWhile(lambda t: any(map(isCaught(t), inp)))(iterate(lambda t: t+1, 1))
print(steps[-1])

# (0, 4), (1, 2), (4, 6), (6, 6) -> 10
