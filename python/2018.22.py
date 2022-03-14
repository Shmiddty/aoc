import sys
import re
from grid import Grid, shortestpath, manhattan
from vector import add


class region(tuple):
    def __str__(self):
        return '.=|'[self[2]]

def geoindex(grid, tx, ty, pt):
    if pt == (0,0): return 0
    if pt == (tx, ty): return 0

    if pt[1] == 0: return pt[0] * 16807
    if pt[0] == 0: return pt[1] * 48271

    ag, ae, at = grid[add(pt, (-1, 0))]
    bg, be, bt = grid[add(pt, (0, -1))]

    return ae * be

def mapcave(depth, tx, ty, maxX = None, maxY = None):
    if maxX == None: maxX = tx
    if maxY == None: maxY = ty
    cave = Grid()

    for y in range(maxX + 1):
        for x in range(maxY + 1):
            pt = (x,y)
            g = geoindex(cave, tx,ty, pt)
            e = (g + depth) % 20183
            t = e % 3
            cave.set(pt, region([g,e,t]))
    return cave

inp = map(int, re.findall(r'\d+', sys.stdin.read()))
# part 1
cave = mapcave(*inp)
risk = sum(map(lambda pt: cave[pt][2], cave))
print(cave)
print(risk)


tx, ty = inp[1:]
cave = mapcave(*inp, maxX = 2*tx, maxY = 2*ty)

# I don't think this approach will work.
def gearscore(cave, start, end):
    sg, se, st = cave[start]
    eg, ee, et = cave[end]

    if st == et: return 0
    return 3.5 # this could be anything, really

path = shortestpath(
        (0,0),
        tuple(inp[1:]),
        neighbors = cave.neighbors,
        isblocked = lambda pt: pt not in cave,
        score = lambda end: lambda start: manhattan(start, end) + gearscore(cave, start, end)
)

pcave = Grid(cave)
for pt in path:
    pcave.set(pt, 'X')
print(pcave)

def mintime(grid, path):
    # try all the things?
    # can't brain right now thinky hard.
    return 0

print(mintime(cave, path))
