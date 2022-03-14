import sys
from functools import partial
from string import words
from func import callWith, pipe

OPS = {
    "inc": lambda a, b: a + b,
    "dec": lambda a, b: a - b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}

def parse(line):
    a, op, v1, iff, b, comp, v2 = words(line)
    return (op, a, int(v1)), (comp, b, int(v2))

def step(state, ((op, a, v1), (comp, b, v2))):
    A = state[a] if a in state else 0
    B = state[b] if b in state else 0
    if OPS[comp](B, v2): state[a] = OPS[op](A, v1)
    return state

inp = [parse(line) for line in sys.stdin]
state = reduce(step, inp, {})
print(max(state.values()))

# this works because step mutates state 
def stepper(state): return lambda fn: dict(fn(partial(step, state)))

states = map(pipe(callWith, stepper({ })), inp)
values = [val for st in states for val in st.values()]

print(max(values))
