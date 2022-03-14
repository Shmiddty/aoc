import sys
from grid import Grid, up, down, left, right, shortestpath, manhattan, multipath
from func import prtl
from enum import flatten

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


# this is too memory intensive
def flat(groups):
    if all(map(lambda s: type(s) == str, groups)):
        return groups

    return reduce(lambda a, b: [A + B for B in flat(b) for A in a], groups, [''])

#def buildmap(inp):
#    themap = Grid(default='#')
#
#    def step((pos, grid), dirs):
#        if type(dirs) == list:
#
#            return map(lambda d: step((pos, grid), d)[0], dirs)
#
#        for d in dirs:
#            D = [up, down, left, right]['NSWE'.index(d)]
#            pos = D(pos)
#            grid.set(pos, 'O')
#            pos = D(pos)
#            grid.set(pos, '.')
#
#        return pos, grid
#
#    return step(((0,0), themap), inp)[1]

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

inp = parse(iter(sys.stdin.read().strip()))
themap = buildmap(inp)
themap.set((0,0), 'X')
#print(themap)

rooms = filter(lambda pt: themap[pt] == '.', themap)
longest = multipath(
    (0,0),
    rooms,
    isblocked = lambda pt: pt not in themap,
    neighbors = themap.neighbors,
    score = lambda end: lambda start: 1.0 / (1 + manhattan(start, end)),
    selector = max
)
print((len(longest) - 1) / 2)
#3644
