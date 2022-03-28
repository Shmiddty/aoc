import sys
from string import digits
from enum import irange

def diff(a, b): return a - b

def step((state, val), i):
    nxt = diff(*(state[val] + [i])[0:2])
    if nxt not in state: state[nxt] = []
    state[nxt] = ([i+1] + state[nxt])[0:2]
    return state, nxt

inp = digits(sys.stdin.read())
count = len(inp)
state0 = dict(map(lambda (i, v): (v, [i + 1]), enumerate(inp)))

state1, part1 = reduce(step, irange(count, 2020), (state0, inp[-1]))
print(part1)

# this is correct, but kinda slow. It does finish, though.
state2, part2 = reduce(step, irange(2020, 3*10**7), (state1, part1))
print(part2)

# so what's the correct way to do this problem?
