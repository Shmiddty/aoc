import sys
from string import digits
from enum import flatten, nth
from grid import Grid, left, right, down, up

def parse(line):
    axis = line[0]
    a, b, c = digits(line)
    return [(a,p) if axis == 'x' else (p, a) for p in range(b, c+1)]

def fill(grid, source = (500, 1), wall = '#', still = '~', flowing = '|'):
    (minx, miny), (maxx, maxy) = grid.bounds()

    water = Grid()

    def filled(pt):
        return pt in grid or (pt in water and water[pt] == still)

    def seekblock(pt, direction):
        out = []
        cur = pt
        while not filled(cur):
            out.append(cur)
            if not filled(down(cur)): # overflow!
                return False, out
            cur = direction(cur)

        return True, out

    def assign(pt, val):
        if miny <= pt[1] <= maxy:
            water[pt] = val

    q = [source]

    while len(q):
        pt = q.pop(0)

        if pt[1] > maxy: continue
        if filled(pt): continue

        dwn = down(pt)
        if not filled(dwn):
            assign(pt, flowing)
            q.append(dwn)
        else:
            l, L = seekblock(left(pt), left)
            r, R = seekblock(right(pt), right)
            for p in L + [pt] + R:
                assign(p, still if l and r else flowing)

            if l and r: q.append(up(pt))
            if not l: q.append(L[-1])
            if not r: q.append(R[-1])

    return water

inp = flatten([parse(line) for line in sys.stdin])

spring = (500, 0)
G = Grid(map(lambda pt: (pt, '#'), inp))
water = fill(G, down(spring))
#merged = G + water
#merged.set(spring, '+')
#print(merged)

# Part 1
print(len(water))

# Part 2
print(len(filter(lambda pt: water[pt] == '~', water)))
