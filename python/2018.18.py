import sys
from grid import Grid, fromString
from func import repeat, iterate

forest = '|'
meadow = '.'
lumber = '#'


def step(grid):
    out = Grid()
    for pt in grid:
        val = grid[pt]

        neigh = map(grid.get, grid.neighbors(pt, True))
        ntree = neigh.count(forest)
        nopen = neigh.count(meadow)
        nlyrd = neigh.count(lumber)

        out.set(pt, val)
        if val == meadow and ntree > 2: out.set(pt, forest)
        if val == forest and nlyrd > 2: out.set(pt, lumber)
        if val == lumber and (nlyrd == 0 or ntree == 0): out.set(pt, meadow)

    return out

def resourcevalue(grid):
    vals = grid.values()
    return vals.count(forest) * vals.count(lumber)

def manystep(grid, N):
    past = []
    cur = grid

    i = 0
    while i < N:
        past.append(cur)
        cur = step(cur)
        i += 1
        if cur in past:
            break

    ri = past.index(cur)
    return past[(N - i) % (i - ri) + ri]

G = fromString(sys.stdin.read())

# Part 1
one = repeat(step, G)(10)
print(resourcevalue(one))

# Part 2
two = manystep(G, 1000000000)
print(resourcevalue(two))

