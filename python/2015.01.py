import sys

inp = [line.strip() for line in sys.stdin][0]

def part1():
    return sum(map(lambda c: 2 * (c == '(') - 1, inp))

print(part1())

def part2():
    floor = 0
    for (i, c) in enumerate(inp):
        floor += 2 * (c == '(') - 1
        if floor < 0:
            return i + 1

print(part2())
