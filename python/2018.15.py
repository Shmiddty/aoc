import sys
import grid
from enum import within, flatten, nth
from func import pipe, prtl, equals, nequals, more, fany, fall, swap, spread, fBa, I, ffs
from grid import manhattan

class Mob:
    def __init__(self, team = "E", power = 3, hp = 200):
        self.hp = hp
        self.team = team
        self.power = power

    def health(self):
        return self.hp

    def __repr__(self):
        return "Mob(%s, %d, %d)"%(self.team, self.power, self.hp)

    def __str__(self):
        return self.team

    def __req__(self, other):
        return self.team == other

    def __eq__(self, other):
        return self.team == other

    def __gt__(self, other):
        return self.hp > other

    def __lt__(self, other):
        return self.hp < other

    def __add__(self, other):
        self.hp += other
        return self

    def __radd__(self, other):
        self.hp += other
        return self

    def __sub__(self, other):
        self.hp -= other
        return self

def initmobs(grid, elfpower = 3, goblinpower = 3):
    for actor in combatants(grid):
        grid[actor] = Mob(grid[actor], elfpower if grid[actor] == 'E' else goblinpower)

    return grid

def combatants(grid):
    return sorted(
        filter(pipe(
            grid.get,
            fany(equals('E'), equals('G')),
            more(0)
        ), grid),
        key=spread(swap) # sort by y, then by x, aka "(western) Reading Order"
    )

# adapted from
# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def shortest(
        start,
        end,
        val = lambda key: key,
        key = lambda key: key,
        isblocked = lambda val: val > 0,
        neighbors = lambda key: grid.orthogonal(key),
        score = lambda end: lambda key: manhattan(key, end)
    ):
    h = score(end)
    gscore = { start: 0 }
    fscore = { start: h(start) }
    q = [start]
    camefrom = {}

    def repath(current):
        path = [current]
        while current in camefrom:
            current = camefrom[current]
            path = [current] + path
        return path

    while len(q):
        cur = q.pop(0)

        if cur == end:
            return repath(cur)

        for neigh in neighbors(cur):
            # neigh != end doesn't really belong here
            if neigh != end and isblocked(val(neigh)):
                continue

            nk = key(neigh)
            scor = gscore[cur] + score(cur)(neigh)
            if nk not in gscore or scor < gscore[nk]:
                camefrom[nk] = cur
                gscore[nk] = scor
                fscore[nk] = scor + h(neigh)
                if neigh not in q:
                    q.append(neigh)
                    # slightly faster with the q properly sorted.
                    q = sorted(q, key=pipe(key, fscore.get))

    return None

def dI(a):
    print(a)
    return a

def domove(grid, actor, target):
    grid[target] = grid[actor]
    grid[actor] = '.'
    return grid

def doattack(grid, actor, target):
    power = grid[actor].power
    grid[target] = grid[target] - power
    if grid[target] < 1: grid[target] = '.'
    return grid

def doturn(grid, actor):
    if grid[actor] == '.': return grid # they done died

    findpath = prtl(
        shortest,
        val=grid.get,
        isblocked=fany(equals('#'), equals('G'), equals('E')),
        neighbors=grid.neighbors,
        # scoring also takes "reading order" into account
        score = lambda end: lambda key: manhattan(end, key)*10**8 + key[1]*10**4 + key[0]
    )
    paths = pipe(
        prtl(filter, fall(nequals(actor), pipe(grid.get, nequals(grid[actor])))),
        prtl(map, grid.neighbors),
        flatten,
        # open space or current destination
        prtl(filter, fany(equals(actor), pipe(grid.get, equals('.')))),
        prtl(map, prtl(findpath, actor)),
        prtl(filter, bool)
    )(combatants(grid))

    if not len(paths): return grid

    closest = min(paths, key=ffs(
        len,                                    # first by path length
        pipe(nth(-1), spread(swap))             # then by (y, x)
    ))

    if len(closest) > 1:
        grid = domove(grid, actor, closest[1])
        actor = closest[1]

    adjacent = pipe(
        grid.neighbors,
        prtl(filter, pipe(grid.get, prtl(prtl, isinstance), prtl(fBa, Mob))),
        prtl(filter, pipe(grid.get, nequals(grid[actor])))
    )(actor)

    if not len(adjacent): return grid

    target = min(adjacent, key=ffs(
        pipe(grid.get, Mob.health),
        spread(swap)
    ))
    doattack(grid, actor, target)

    return grid

def doround(grid, i):
    actors = combatants(grid)
    alive = map(grid.get, actors)
    for actor in actors:
        alive = filter(pipe(Mob.health, more(0)), alive)
        if all(map(equals('E'), alive)) or all(map(equals('G'), alive)):
            return grid, i

        grid = doturn(grid, actor)

    return grid, i + 1

def docombat(grid):
    i = 0
    while True:
        #print(grid)
        #print('')
        grid, inxt = doround(grid, i)
        if i == inxt: return grid, i
        i = inxt

def winninghealth(grid):
    return sum(map(pipe(grid.get, Mob.health), combatants(grid)))

def outcome(grid, rounds):
    return rounds * winninghealth(grid)

ginit = grid.fromString(sys.stdin.read())
print(outcome(*docombat(initmobs(grid.Grid(ginit)))))

def numelves(grid):
    return len(filter(pipe(grid.get, equals('E')), grid))

def part2(ginit):
    N = numelves(ginit)
    power = 4
    # could probably save some cycles by starting this at a
    # smarter value based on the ratio of elves to goblins
    # could also end combat as soon as an elf dies, but that'd require more hacky bits
    while True:
        g = initmobs(grid.Grid(ginit), power)
        g, rnds = docombat(g)
        if numelves(g) == N:
            print(g)
            return outcome(g, rnds)
        power += 1

print(part2(ginit))
