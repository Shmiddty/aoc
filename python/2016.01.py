import sys

sys.path.insert(0, './lib/')
import vector as V
import grid as G
import maths as M
import enum as E 
import func as F
from functools import partial

inp = [(v[0], int(v[1:])) for v in sys.stdin.read().split(', ')]

#def step((t, d)):
#    def fn((p, f)):
#        f = G.turnLeft(f) if t == "L" else G.turnRight(f)
#        return (V.add(p, V.scale(d, f)), f) 
#    return fn
#
#pos, fac = reduce(lambda o, f: f(o), map(step, inp), ((0,0), (0, 1))) 
#print(G.manhattan((0,0), pos))

def step2((t, d)):
    def fn((p, f)):
        f = G.turnLeft(f) if t == "L" else G.turnRight(f)
        return map(lambda v: (v, f), F.iterN(partial(V.add, f), d)(p))[1:]
    
    return fn  

steps = reduce(lambda o, f: o + f(o[-1]), map(step2, inp), [((0,0), (0, 1))])
pos, fac = steps[-1]
print(G.manhattan((0,0), pos))
P = map(E.nth(0), steps)
reps = map(E.nth(1), filter(lambda (i, p): p in P[0:i], enumerate(P)))
print(G.manhattan((0,0), reps[0]))
