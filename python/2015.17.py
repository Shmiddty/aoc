import sys
from itertools import combinations 
from enum import flatten, nth, without, aggregate
from func import pipe

inp = list(enumerate([int(line.strip()) for line in sys.stdin]))

def checker(n):
    return lambda ls: sum(map(nth(1), ls)) == n

def part1(n = 150):
    return filter(
        checker(n),
        [c for n in range(2, len(inp) + 1) for c in combinations(inp, n)]
    )

print(len(part1()))

def part2(n = 150):
    a = aggregate(map(len, part1(n))) # maybe I should stop wasting cpu cycles, eh? 
    return a[min(a)]

print(part2())
