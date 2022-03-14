import sys
from enum import nth
from func import pipe

inp = sys.stdin.read().strip()

def matches(ls, offset):
    pairs = zip(inp, inp[offset:] + inp[0:offset])
    matching = filter(lambda (a, b): a == b, pairs)
    return map(pipe(nth(0), int), matching)

print(sum(matches(inp, 1)))
print(sum(matches(inp, len(inp) / 2)))
