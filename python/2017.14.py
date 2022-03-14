import sys
from functools import partial as curry

import knot
from bits import hextobits
from enum import flatten, at
from string import concat
from func import pipe
from grid import orthogonal

inp = sys.stdin.read().strip()

# this is kinda slow
bitgrid = map(
    pipe(
        curry(concat, inp, '-'), 
        knot.hashstr,
        curry(map, hextobits),
        flatten
    ),
    range(128)
)

gridstring = '\n'.join(map(
    pipe(
        curry(map, at('.#')), 
        ''.join
    ),
    bitgrid
))

#print(gridstring)

print(sum(map(sum, bitgrid)))

# this might be a good candidate for generalization. 
def getRegions(grid):
    visited = {} 
    def seek(pt):
        x, y = pt
        if y < 0 or y >= len(grid): return []
        if x < 0 or x >= len(grid[y]): return []

        val = grid[y][x]
        
        if val == 0 or pt in visited: return []
        
        visited[pt] = 1

        return flatten([pt] + map(seek, orthogonal(pt)))

    return filter(len, [seek((x,y))
        for (y, row) in enumerate(grid)
        for (x, col) in enumerate(row)
        if (x,y) not in visited
        # it appears that this is evaluated at each step after the seek from the previous step. Cool.
    ])

regions = getRegions(bitgrid)
#print(regions)
print(len(regions))
