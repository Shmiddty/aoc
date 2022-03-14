import sys
import re

inp = sys.stdin.read()

def part1():
    return sum(map(int, re.findall(r'-?\d+', inp)))

print(part1())

# part2 will require a JSON parser.
