import sys
from functools import partial

from vector import add
from func import pipe, over

#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \

#    NW        N
#  ( 0,  1) ( 1,  1) 
#    SW        O        NE
#  (-1,  0) ( 0,  0) ( 1,  0)
#              S        SE 
#           (-1, -1) ( 0, -1)


# -2: [ 0,  1,  2,  3,  4]
# -1: [-1,  0,  1,  2,  3]
#  0: [-2, -1,  0,  1,  2]
#  1: [-3, -2, -1,  0,  1]
#  2: [-4, -3, -2, -1,  0]

#      -3  -2  -1   0   1   2  3
#  3: [ 3,  3,  3,  3,  4,  5, 6]
#  2: [ 3,  2,  2,  2,  3,  4, 5]
#  1: [ 3,  2,  1,  1,  2,  3, 4]
#  0: [ 3,  2,  1,  *,  1,  2, 3]
# -1: [ 4,  3,  2,  1,  1,  2, 3]
# -2: [ 5,  4,  3,  2,  2,  2, 3]
# -3: [ 6,  5,  4,  3,  3,  3, 3]
# taxicab measurement for hex grid
# I think this only works for the origin case
def dist((x1, y1), (x2, y2)): return max(abs(x2 - x1), abs(y2 - y1))

def delta(d):
    return {
        'ne': ( 1,  0),
        'nw': ( 0,  1),
        'se': ( 0, -1),
        'sw': (-1,  0),
        'n':  ( 1,  1),
        's':  (-1, -1)
    }[d]

inp = sys.stdin.read().strip().split(',')

orig = (0, 0)
dest = reduce(add, map(delta, inp), orig)
print(dist(orig, dest))

steps = over(*map(pipe(delta, partial(partial, add)), inp))(orig)
dists = map(partial(dist, orig), steps)
print(max(dists))
