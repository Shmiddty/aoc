import sys
from grid import manhattan
from string import digits
from enum import nth, take, irange
from func import prtl, pipe, less
from region import containing, ipoints3d

inp = [digits(line) for line in sys.stdin]
nanohercules = max(inp, key=nth(3))
x, y, z, rnge = nanohercules
dist = prtl(manhattan, (x,y,z))

# Part 1
inrange = filter(pipe(take(3), dist, less(rnge)), inp)
print(len(inrange))

def part2():
    maxbots = -sys.maxint
    mindist = sys.maxint
    # too slow 
    for pt in ipoints3d(containing(map(take(3), inp))):
        dist = prtl(manhattan, pt)
        dorig = dist((0,0,0))

        botcount = len(filter(lambda (X,Y,Z,R): dist((X,Y,Z)) <= R, inp))
        
        if botcount > maxbots:
            mindist = dorig
            maxbots = botcount
        elif botcount == maxbots and mindist > dorig:
            mindist = dorig

    return mindist

print(part2())
