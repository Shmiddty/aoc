import sys
import re
from enum import nth, partition
from grid import Grid, shortestpath, manhattan, orthogonal
from vector import add
from func import memo
from region import points2d

#class reg(tuple):
#    def __str__(self):
#        return '.=|'[self[2]]
#
#def geoindex(grid, tx, ty, pt):
#    if pt == (0,0): return 0
#    if pt == (tx, ty): return 0
#
#    x, y = pt
#
#    if y == 0: return x * 16807
#    if x == 0: return y * 48271
#
#    ag, ae, at = grid[add(pt, (-1, 0))]
#    bg, be, bt = grid[add(pt, (0, -1))]
#
#    return ae * be
#
#def mapcave(depth, tx, ty, maxX = None, maxY = None):
#    if maxX == None: maxX = tx
#    if maxY == None: maxY = ty
#    cave = Grid()
#
#    for y in range(maxY + 1):
#        for x in range(maxX + 1):
#            pt = (x,y)
#            g = geoindex(cave, tx,ty, pt)
#            e = (g + depth) % 20183
#            t = e % 3
#            cave.set(pt, reg([g,e,t]))
#    return cave

def makecave(depth, tx, ty):
    def geoindex(pt):
        x, y = pt
        if x < 0 or y < 0: return sys.maxint

        if pt == (0,0): return 0
        if pt == (tx, ty): return 0
        if y == 0: return x * 16807
        if x == 0: return y * 48271

        return merosion(add(pt, (0, -1))) * merosion(add(pt, (-1, 0)))

    mgeoindex = memo(geoindex)
    
    def erosion(pt):
        return (mgeoindex(pt) + depth) % 20183

    merosion = memo(erosion)

    def regiontype(pt):
        return merosion(pt) % 3

    mregiontype = memo(regiontype)

    return mregiontype


inp = map(int, re.findall(r'\d+', sys.stdin.read()))
d, tx, ty = inp
regtype = makecave(d, tx, ty)

# part 1
#cave = mapcave(d, tx, ty)
#risk = sum(map(lambda pt: cave[pt][2], cave))
#print(cave)
risk = sum(map(regtype, points2d(((0,0), (tx, ty)))))
print(risk)

#pad = 57#23
#cave = mapcave(d, tx, ty, maxX = tx + pad, maxY = ty + pad)

neither, torch, gear = 0, 1, 2
rocky, wet, narrow = 0, 1, 2
regtools = {
    rocky:[torch, gear],
    wet:[neither, gear],
    narrow:[neither, torch]
}

pad = 70
path = shortestpath(
    ((0,0), torch),
    ((tx, ty), torch),
    # the problem is here. I have the rules close, but not quite correct.
    # you can only move if the next region accepts your current tool.
    # that is, you can't switch tools in the next region if it doesn't allow your current tool
    neighbors = lambda (pt, tl): [
        ((x,y), tool)
        for (x,y) in orthogonal(pt)#cave.neighbors(pt)
        for tool in regtools[regtype((x,y))]# cave[neighbor][2]]
        if x >= 0 and y >= 0 and x <= tx * 7 and# y < ty + pad and
            (regtype(pt) == regtype((x,y)) or tl in regtools[regtype((x,y))])
    ],
    isblocked = lambda (pt, _): False,
    score = lambda (end, toolEnd): lambda (start, toolStart):(
        manhattan(start, end) + (toolEnd != toolStart) * 7
    )
)
#pcave = Grid(cave)
#for (pt, t) in path:
#    pcave.set(pt, 'OX@'[t])
#print(pcave)
#print(map(lambda (pt, tool): (pt, cave[pt][2], tool), path))
#print(Grid(path))

toolswaps = len(partition(map(nth(1), path))) - 1
#print(toolswaps, len(path))
print(7 * toolswaps + len(path) - 1)
#995 is too low...
#997 is also too low?
#1023 is too high
# 1000?
# 1006? nope.
# 1007?
# 1008? nope.
# 1020? nope.
# 1004 is probably the right answer
