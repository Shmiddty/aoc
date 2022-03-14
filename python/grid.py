from functools import partial

from vector import add
from func import iterN, prtl, pipe,ffs
from enum import within, without

from region import containing

def turn((x, y)):
    return (-y, x)

def turnLeft(a):
    return turn(a)

def turnRight(a):
    return turn(turn(turn(a)))

def manhattan(a, b):
    return sum(map(lambda (c,d): abs(d - c), zip(a,b))) 

# it's a pun!
fourtune = iterN(turn, 3)
orth = fourtune((0,1))
diag = fourtune((1,1))

left  = prtl(add, (-1,  0))
right = prtl(add, ( 1,  0))
up    = prtl(add, ( 0, -1))
down  = prtl(add, ( 0,  1))

def orthogonal(pt): return map(partial(add, pt), orth)
def diagonal(pt): return map(partial(add, pt), diag)

class Grid(dict):
    def __init__(self, items = [], default = ' '):
        dict.__init__(self, items)
        self.default = default

    def set(self, pt, val):
        self[pt] = val
        return self

    def neighbors(self, pt, includeDiagonal = False):
        return filter(
            within(self), # only grab neighbors that exist
            orthogonal(pt) + (diagonal(pt) if includeDiagonal else [])
        )

    def bounds(self):
        return containing(self.keys())

    def __radd__(self, other):
        return Grid(other.items() + self.items(), other.default)
    def __add__(self, other):
        return Grid(self.items() + other.items(), self.default)

    def __str__(self):
        (x0, y0), (x1, y1) = containing(self.keys())
        return '\n'.join([
            ''.join([
                str(self[(x,y)]) if (x,y) in self else str(self.default)
                for x in range(x0, x1+1)
            ])
            for y in range(y0, y1+1)
        ])

def fromString(string):
    return Grid([
        ((x,y), c)
        for (y, row) in enumerate(string.strip().split('\n'))
        for (x, c) in enumerate(row)
    ])

def shortestpath(
        start,
        target,
        val = lambda key: key,
        key = lambda key: key,
        isblocked = lambda val: val > 0,
        neighbors = lambda key: orthogonal(key),
        score = lambda end: lambda key: manhattan(key, end)
    ):
    h = score(target)
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

        if cur == target:
            return repath(cur)

        for neigh in neighbors(cur):
            if isblocked(val(neigh)):
                continue

            nk = key(neigh)
            scor = gscore[cur] + score(cur)(neigh)
            if nk not in gscore or scor < gscore[nk]:
                camefrom[nk] = cur
                gscore[nk] = scor
                fscore[nk] = scor + h(neigh)
                if neigh not in q:
                    q.append(neigh)
                    # slightly faster with the q sorted.
                    q = sorted(q, key=pipe(key, fscore.get))

    return None

def multipath(
        start,
        targets,
        val = lambda key: key,
        key = lambda key: key,
        isblocked = lambda val: val > 0,
        neighbors = lambda key: orthogonal(key),
        score = lambda end: lambda key: manhattan(key, end),
        selector = min
    ):
    remaining = list(targets)
    h = pipe(ffs(*map(prtl(score), targets)), min)
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

        if cur in remaining:
            remaining = without(remaining, remaining.index(cur))
            if len(remaining) == 0:
                return repath(selector(fscore, key=gscore.get))

        for neigh in neighbors(cur):
            if isblocked(val(neigh)):
                continue

            nk = key(neigh)
            scor = gscore[cur] + score(cur)(neigh)
            if nk not in gscore or scor < gscore[nk]:
                camefrom[nk] = cur
                gscore[nk] = scor
                fscore[nk] = scor + h(neigh)
                if neigh not in q:
                    q.append(neigh)
                    q = sorted(q, key=pipe(key, fscore.get))

    return None


