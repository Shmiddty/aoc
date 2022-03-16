import sys
from grid import Grid, up, down, left, right, shortestpath, manhattan
from func import prtl
from enum import flatten

# this is very awkward and I don't like it
def parse(iinp):
    acc = ['']
    while True:
        val = next(iinp)
        if val == '^':
            continue
        if val == '$':
            return flatten(acc)

        if val == ')':
            if type(acc[-1]) == list and acc[-1][-1] == '': # this is icky
                acc[-1].pop()
            return acc

        if val == '(':
            if type(acc[-1]) == list:
                acc[-1] = acc[-1] + [parse(iinp)] + ['']
            else:
                acc[-1] = [acc[-1], parse(iinp), '']
        elif val == '|':
            if type(acc[-1]) == list and acc[-1][-1] == '': # this is icky
                acc[-1].pop()
            acc.append('')
        else:
            if type(acc[-1]) == list: # this is icky
                acc[-1][-1] += val
            else:
                acc[-1] += val

# this is awkward and I don't like it.
def buildmap(inp):
    themap = Grid(default = '#')

    def move(pos, d):
        D = [up, down, left, right]['NSWE'.index(d)]
        pos = D(pos)
        themap.set(pos, 'O')
        pos = D(pos)
        themap.set(pos, '.')
        return pos

    def step(poss, groups):
        if not len(groups): return poss

        for group in groups:
            if type(group) == str:
                poss = [reduce(move, group, pos) for pos in poss]
            else:
                poss = flatten(map(prtl(step, poss), group))

        return list(set(poss)) # no reason to travel the same path more than once

    step([(0,0)], inp)
    return themap

def doors(grid, origin = (0,0)):
    class num(int):
        def __str__(self):
            return int.__str__(self).center(4, ' ')
    
    doorscore = Grid([(origin, num(0))], default="....")
    q = [origin]

    while len(q):
        cur = q.pop(0)
        score = doorscore[cur]

        for Dir in [up, down, left, right]:
            if Dir(cur) in grid: # we have a door
                room = Dir(Dir(cur))
                roomscore = score + 1

                if room not in doorscore or doorscore[room] > roomscore:
                    doorscore[room] = num(roomscore)
                    q.append(room)
    
    return doorscore

inp = parse(iter(sys.stdin.read().strip()))
themap = buildmap(inp)
themap.set((0,0), 'X')

doorscores = doors(themap)
#print(doorscores)

# Part 1
print(max(doorscores.values())) #3644

# Part 2
print(len(filter(lambda v: v > 999, doorscores.values()))) # 8523

