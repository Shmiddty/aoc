import sys

from grid import Grid, turnLeft, turnRight
from vector import add
from func import spread, pipe
from enum import nth, irange

# 0,0 is the top left... hmm
init = Grid([
    ((x, y), int(c == '#'))
    for (y, row) in enumerate(sys.stdin)
    for (x, c) in enumerate(row.strip())
])
width, height = add(max(init), (1,1))
origin = (width / 2, height / 2)
up = (0, -1)

def debug(grid, vals = '.#'):
    xs, ys = zip(*grid)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for y in range(miny, maxy + 1):
        s = ''
        for x in range(minx, maxx + 1):
            pt = (x,y)
            s += vals[grid[pt]] if pt in grid else vals[0]
        print(s)            
    print('')

def stepper(left = turnLeft, right = turnRight, r = 2):
    def step(grid, pos, fac, n):
        # default value is 0. it'd be nice to have that in the grid constructor 
        # might have to move away from inheriting from dict for my infinite grid
        if pos not in grid: grid[pos] = 0

        state = grid[pos]

        # and that's why I wanted to keep 
        fac = [
            left(fac),      # clean
            fac,            # weakened
            right(fac),     # infected 
            left(left(fac)) # flagged
        ][state * 4 / r]    # this is hacky, but it
        # maps 1 to 2 if r == 2, all other values should be unaffected
        # this assumes r = 2 and r = 4 are the only valid options
        # which is a safe assumption, since this is just code for a toy problem
        
        grid[pos] = (state + 1) % r
    
        return grid, add(pos, fac), fac, n + (grid[pos] == r / 2)
    
    return step

def nsteps(n, g0, p0, f0, left = turnLeft, right = turnRight, r = 2, D = False):
    step = stepper(left, right, r)
    
    # more icky hacky things. 
    # this fixes the grid so that 2 is infected instead of 1
    # I tried to think of a way to keep 1 as infected 
    # but I also wanted to avoid boolean logic as much as possible
    if r == 4:
        for pt in g0: g0[pt] = 2 * g0[pt]

    def dbg(*args):
        if D: debug(args[0], '.#' if r == 2 else '.W#F')
        return step(*args) 

    return reduce(
        lambda o, _: dbg(*o),
        irange(n),
        (g0, p0, f0, 0)
    )

g1, p1, f1, n1 = nsteps(
    10000,              # ten thousand steps
    Grid(init),         # clone the inital grid since we're relying on mutations
    origin,             # start at the origin
    up,                 # facing up 
    turnRight,          # left is actually right since postive y is down 
    turnLeft,           # and right is left
    2                   # clean -> infected -> clean
)

# part 1
print(n1)

# this is kinda slow. there must be some other way to approach it
g2, p2, f2, n2 = nsteps(
    10**7,              # ten million steps
    Grid(init),         # clone the inital grid since we're relying on mutations
    origin,             # start at the origin
    up,                 # facing up 
    turnRight,          # left is actually right since postive y is down 
    turnLeft,           # and right is left
    4                   # clean -> weakened -> infected -> flagged -> clean
)

# part 2
print(n2)
# 2511865 is too low. Not sure what is wrong
# the problem was that I did not update my initial grid values
# so that 2 represents the initial infected spaces
# really this is all very awkward and I should have found a way to keep 1 as the infected value
