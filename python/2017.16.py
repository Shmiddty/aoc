import sys
from functools import partial

from string import tokens, concat
from enum import rotate, swap, swapval, circular, takeWhile
from func import pipe, withresult, iterate, nequals, repeat
from maths import add

OPS = {
    's': rotate,
    'x': swap,
    'p': swapval,
}

def parseOp(st):
    op = st[0]
    b = st[1:].split('/') if '/' in st else [-int(st[1:])]
    if op == 'x': b = map(int, b)
    return op, b 

inp = map(parseOp, tokens(sys.stdin.read().strip(), ','))

def step(st, (op, b)): return OPS[op](st, *b)

# example
#initial = ''.join(map(pipe(add(97), chr), range(5)))
#print(reduce(lambda o, (op, b): o + [OPS[op](o[-1], *b)], inp, [initial]))

initial = concat(*map(pipe(partial(add, 97), chr), range(16)))
# original part 1
#print(reduce(step, inp, initial))

# to perform the dance a billion times... is there a better way?
# perhaps... check if the value repeats at some point?

# let's try to run the whole thing first
# yeah... this doesn't finish in a reasonable time
#order = repeat(
#    pipe(
#        partial(partial, step),
#        withresult(partial(next, iter(circular(inp))))
#    ),
#    initial
#)(len(inp) * 10**9)
#print(order)

# let's make an iterator so we can accumulate values
routine = iterate( 
    pipe(
        partial(partial, step), # I'm becoming rather partial to partial partials
        # new tool to call a function with the result of another function
        # this allows me to pull values in from an iterator
        withresult(partial(next, iter(circular(inp)))) # glad to see my circular list holds up. first try!
    ),
    initial
)

next(routine) # discard the initial positions

# perform the dance once
waltz = [next(routine) for _ in inp]
# part1
print(waltz[-1])

# accumulate the positions after each step until we find the initial position
steps = takeWhile(nequals(initial))(routine)
L = len(inp) # number of steps in a single dance
R = L + len(steps)  # we add L because they've danced once already
# after 42 dances, the dancers are in their starting positions
N = 10**9 * L
T = N / R       # repeats T times
Tr = N % R      # with a remainder of Tr dances
o = R - Tr      # so... steps[Tr - L] should be the final step?
print(steps[Tr - L - 1]) # fjpmholcibdgeakn, This is correct. silly off-by-ones
#print(steps[Tr - L + 1]) # kndjpmholcibfgea, this is wrong again. 
#print(steps[Tr - L]) # djpmholcibfgeakn, this is wrong
#print(steps[Tr]) # kdpecbfogjilmahn, this is wrong
