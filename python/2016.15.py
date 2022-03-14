import sys
import re
from enum import nth, takeWhile
from func import iterate, equals, less, pipe
from functools import partial
from maths import add

inp = [map(int, re.findall(r'\d+', line)) for line in sys.stdin]

# this assumes:
#  * enum is an enum of generators
#  * enum is sorted by the rate at wich each generator grows in descending order 
#  * each generator is constructed in ascending order
def inEvery(enum, v):
    return len(enum) == 0 or (
        # is v in the first generator?
        takeWhile(less(v))(enum[0])[-1] == v
        and
        # if so, check the next one, and so on...
        inEvery(enum[1:], v)
    )

def findTime(inp):
    # adjust the starting position of each disc by its ordinal
    # so that we can find a time when all of their positions will be zero 
    at0 = map(lambda (o,n,z,p): (p + o - 1, n), inp)
    # sort our zero'd discs by step size, descending
    zed = sorted(at0, key=nth(1), reverse=True)
    # create some generators 
    times = map(lambda (p, n): iterate(partial(add, n), n - p), zed)
    # and I'll form the head.
    anchor = times[0]
    # create an iterator that stops when we find a value that is inEvery generator
    seek = takeWhile(pipe(partial(inEvery, times[1:]), equals(False)))
    # use that iterator to expand the anchor generator and then pop pop!
    return seek(anchor).pop() - 1 # minus the one second to reach the first disc

print(findTime(inp))
print(findTime(inp + [(len(inp) + 1, 11, 0, 0)]))
