import sys
import re

def parseLine(line):
    state = 2 if "toggle" in line else int("on" in line)
    x0, y0, x1, y1 = map(int, re.findall(r'\d+', line))

    return (state, ((x0, y0), (x1, y1)))

inp = [parseLine(line.strip()) for line in sys.stdin]

# kinda slow. Maybe inclusion/exclusion could work
# but I'm not sure how to model the toggle.
def step1(grid, (state, ((x0, y0), (x1, y1)))):
    for pt in [(x,y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]:
        grid[pt] = {
            0: 0,
            1: 1,
            2: 1 if pt not in grid or grid[pt] == 0 else 0
        }[state]
     
    return grid

def part1(ops):
    grid = {}
    for op in ops: step1(grid, op)
    return sum(grid.values())

print(part1(inp))

def step2(grid, (state, ((x0, y0), (x1, y1)))):
    for pt in [(x,y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]:
        val = grid[pt] if pt in grid else 0
        grid[pt] = {
            0: max(0, val - 1),
            1: val + 1,
            2: val + 2
        }[state]

    return grid
 
def part2(ops):
    grid = {}
    for op in ops: step2(grid, op)
    return sum(grid.values())

print(part2(inp))
