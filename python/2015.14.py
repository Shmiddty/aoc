import sys
import re
from enum import aggregate

def parseLine(line):
    name = line.split(' ')[0]
    speed, duration, rest = map(int, re.findall(r'(\d+)', line))
    return (name, speed, duration, rest)

inp = [parseLine(line.strip()) for line in sys.stdin]

def dance(time):
    # a reindeer has no name 
    def f((_, speed, duration, rest)):
        t = time
        d = 0
        while t >= duration + rest:
            d += speed * duration
            t -= duration + rest

        d += speed * min(duration, t)

        return d

    return f

def part1(time = 2503):
    return max(map(dance(time), inp))

print(part1())

def maxxy(ls):
    return lambda k: max(ls, key=k)

def part2(time = 2503):
    # still wrong, apparently
    # I'm getting 688 for Dancer at 1000 seconds for the test input (instead of 689)
    # However, I am getting the correct value of 312 for Comet. 
    return max(
        aggregate(
            map(maxxy(inp), map(dance, range(1, time + 1)))
        ).values()
    )

# 1064 is incorrect

print(part2())#1000))
