import sys
from itertools import permutations, combinations

inp = [map(int, line.split("x")) for line in sys.stdin]

def product(enum):
    return reduce(lambda o, v: o * v, enum, 1)

def paper(dim):
    S = areas(dim)
    return sum(S) + min(S)

def areas(dim):
    return map(product, permutations(dim, 2))

def part1():
    return sum(map(paper, inp)) 

print(part1())

def ribbon(dim):
    P = perimeters(dim)
    return min(P) + product(dim) 

def perimeters(dim):
    return map(lambda (a,b): 2*a + 2*b, combinations(dim, 2))

def part2():
    return sum(map(ribbon, inp)) 

print(part2())
