import sys

from vector import add
from grid import turnLeft, turnRight

grid = [line[0:-1] for line in sys.stdin] # if you strip the line, you're going to have a bad time
origin = (grid[0].index('|'), 0)    # the start of the... labyrinth

def traverse(grid, origin):
    def get((x, y)): 
        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]): return ' '
        return grid[y][x]

    letters = []
    pos = origin
    val = get(origin)
    direction = (0, 1)
    prev = '|'
    steps = 0
    while val != ' ':
        steps += 1
        pos = add(pos, direction)
        val = get(pos)
        
        # a letter
        if val.isupper(): letters.append(val)
       
        # a turn
        if val == '+':
            # I think, technically, left and right are swapped, but it shouldn't matter
            left = turnLeft(direction)
            rght = turnRight(direction)
            if get(add(pos, left)) != ' ': direction = left
            if get(add(pos, rght)) != ' ': direction = rght
            prev = '-' if prev == '|' else '|'

    return ''.join(letters), steps

word, steps = traverse(grid, origin)
print(word)  # part 1
print(steps) # part 2
