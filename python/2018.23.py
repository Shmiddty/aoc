import sys
from grid import manhattan
from vector import diff, add, scale, magnitude
from string import digits
from enum import nth, take, irange, without
from func import prtl, pipe, less, equals, juxt
from region import containing, ipoints3d
from maths import minmax

inp = [digits(line) for line in sys.stdin]


# Part 1
nanohercules = max(inp, key=nth(3))
x, y, z, rnge = nanohercules
dist = prtl(manhattan, (x,y,z))
inrange = filter(pipe(take(3), dist, less(rnge)), inp)
print(len(inrange))

#def part2():
#    maxbots = -sys.maxint
#    mindist = sys.maxint
#    # too slow
#    for pt in ipoints3d(containing(map(take(3), inp))):
#        dist = prtl(manhattan, pt)
#        dorig = dist((0,0,0))
#
#        botcount = len(filter(lambda (X,Y,Z,R): dist((X,Y,Z)) <= R, inp))
#
#        if botcount > maxbots:
#            mindist = dorig
#            maxbots = botcount
#        elif botcount == maxbots and mindist > dorig:
#            mindist = dorig
#
#    return mindist
#
#print(part2())

def dbg(n):
    print(n)
    return n

def intersects((p0, r0), (p1, r1)):
    return manhattan(p0, p1) <= r0 + r1

# also too slow
#print(pipe(
#    prtl(map, juxt(take(3), nth(-1))), # (x,y,z,r) -> ((x,y,z), r)
#    lambda inputs: map(
#        lambda v: reduce(
#            lambda pts, (p1, r1): pts + [(p1, r1)]
#                if all(map(prtl(intersects, (p1, r1)), pts))
#                else pts
#            ,
#            inputs,
#            [v]
#        ),
#        inputs
#    ),
#    prtl(max, key=len),
#    len
#)(inp))

# perhaps:
# set the cursor to the origin
# move the cursor toward each nanobot based on the nanobot's range and its distance from the cursor
# continue these movements until the cursor stabilizes at a single point

PI = 3.14159
def attract(cur, bots):
    rs = sorted(map(nth(1), bots))[1:-1]
    a, b = minmax(rs)
    R = a + b
    # this is too imprecise
    return reduce(
        add,
        map(
            lambda (pt, r): map(
                round,
                scale(
                    R / (PI + magnitude(diff(cur, pt))) / (r),
                    diff(pt, cur)
                )
            ),
            bots
            #filter(pipe(prtl(intersects, (cur, 0)), equals(False)), bots)
        ),
        cur
    )

def simulate(bots):
    cur = (0, 0, 0)
    prev = []
    while cur not in prev:
        prev.append(cur)
        cur = attract(cur, bots)

    print(prev[prev.index(cur):])
    return cur

bts = map(juxt(take(3), nth(-1)), inp)
simulate(bts)

# perhaps:

# set the cursor to the midpoint between all nanobots
# from the nanobots of which the cursor is not in range
# remove that which is furthest from the cursor
# repeat this process unless no nanobot was removed

#def center(pts):
#    minima, maxima = containing(pts)
#    return map(round, add(minima, scale(1.0/2, diff(maxima, minima))))
#
## this is wrong.
#def dropfar(bots):
#    cur = (center(map(nth(0), bots)), 0)
#    print(cur)
#    distance = prtl(manhattan, cur[0])
#    # less(1) is functionally equivalent to equals(False) when a boolean is expected
#    outsiders = filter(pipe(nth(1), prtl(intersects, cur), equals(False)), enumerate(bots)),
#    if not len(outsiders): return bots
#
#    dropI, _ = max(
#        outsiders,
#        key=pipe(nth(1), nth(0), distance)
#    )
#    return without(bots, dropI)
#
#def seek(bots):
#    cur = bots
#    nxt = None
#    while cur != nxt:
#        nxt = cur
#        cur = dropfar(bots)
#
#    return cur
#
#bts = map(juxt(take(3), nth(-1)), inp)
#print(seek(bts))
