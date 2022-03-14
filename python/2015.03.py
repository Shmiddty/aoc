import sys
from vector import add
from enum import at

inp = [line.strip() for line in sys.stdin][0]

def getDir(c):
    return {
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1),
        '<': (-1, 0)
    }[c]

def deliver(steps, grid = None):
    if grid == None: grid = {}
    pos = (0,0)
    grid[pos] = 1
    for d in steps:
        pos = add(pos, d)
        grid[pos] = grid[pos] + 1 if pos in grid else 1

    return grid

def part1():
    return len(deliver(map(getDir, inp)))

print(part1())

def part2():
    steps = map(getDir, inp)
    S = map(at(steps), range(0, len(steps), 2))
    R = map(at(steps), range(1, len(steps), 2)) 
    return len(deliver(R, deliver(S)))

print(part2())
