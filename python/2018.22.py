import sys
import re
from enum import nth, partition
from grid import Grid, shortestpath, manhattan, orthogonal
from vector import add
from func import memo
from region import points2d

def makecave(depth, tx, ty):
    def geoindex(pt):
        x, y = pt
        if x < 0 or y < 0: return 0

        if pt == (0,0): return 0
        if pt == (tx, ty): return 0
        if y == 0: return x * 16807
        if x == 0: return y * 48271

        return merosion(add(pt, (-1, 0))) * merosion(add(pt, (0, -1)))

    def erosion(pt):
        return (mgeoindex(pt) + depth) % 20183

    def regiontype(pt):
        return merosion(pt) % 3

    mgeoindex = memo(geoindex)
    merosion = memo(erosion)
    mregiontype = memo(regiontype)

    class Region(int):
        def __str__(self):
            return '.=|#'[self]

    class Cave(Grid):
        def __getitem__(self, key):
            if key[0] < 0 or key[1] < 0: return 0 # not ideal but does the job.

            if key not in self:
                self[key] = Region(mregiontype(key))

            return dict.__getitem__(self, key)
        def get(self, key):
            return self.__getitem__(key)

    return Cave()

inp = map(int, re.findall(r'\d+', sys.stdin.read()))
d, tx, ty = inp
cave = makecave(d, tx, ty)

# part 1
risk = sum(map(cave.get, points2d(((0,0), (tx, ty)))))
print(risk)

#print(cave)

neither, torch, gear = 0, 1, 2
rocky, wet, narrow = 0, 1, 2
regtools = {
    rocky:[torch, gear],
    wet:[neither, gear],
    narrow:[neither, torch]
}

# Part 2
path = shortestpath(
    ((0,0), torch),
    ((tx, ty), torch),
    neighbors = lambda (pt, tl): [
        ((x,y), tool)
        for (x,y) in orthogonal(pt)
        for tool in regtools[cave[(x,y)]]
        if x >= 0 and y >= 0 and x <= tx * 5 and
            # x <= tx * 5 is kinda arbitrary and it would be nice
            # to get rid of it in favor of a smartly-expanding area
            # but I haven't been able to figure out how to do that
            tl in regtools[cave[(x,y)]]
    ],
    isblocked = lambda (pt, _): False,
    score = lambda (end, toolEnd): lambda (start, toolStart):(
        manhattan(start, end) + (toolEnd != toolStart) * 7
    )
)
#print('')
#print(cave)
toolswaps = len(partition(map(nth(1), path))) - 1
print(7 * toolswaps + len(path) - 1)
