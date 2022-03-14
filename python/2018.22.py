import sys
import re
from enum import nth, partition
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

    for y in range(maxY + 1):
        for x in range(maxX + 1):
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
#print(cave)
print(risk)

tx, ty = inp[1:]
cave = mapcave(*inp, maxX = 2*tx, maxY = 2*ty)

neither, torch, gear = 0, 1, 2
rocky, wet, narrow = 0, 1, 2
regtools = {
    rocky:[torch, gear],
    wet:[neither, gear],
    narrow:[neither, torch]
}

path = shortestpath(
    ((0,0), torch),
    (tuple(inp[1:]), torch),
    neighbors = lambda (pt, _): [
            (neighbor, tool)
            for neighbor in cave.neighbors(pt)
            for tool in regtools[cave[neighbor][2]]
        ],
    isblocked = lambda (pt, _): pt not in cave,
    score = lambda (end, te): lambda (start, ts):(
            manhattan(start, end) + (te != ts) * 7
        )
)

#pcave = Grid(cave)
#for (pt, t) in path:
#    pcave.set(pt, 'X')
#print(pcave)
toolswaps = len(partition(map(nth(1), path))) - 1
print(7 * toolswaps + len(path) - 1)
