import sys
from functools import reduce
import re
from maths import add

def wordToDigit(n):
    vals = {
        'zero':0,
        'one':1,
        'two':2,
        'three':3,
        'four':4,
        'five':5,
        'six':6,
        'seven':7,
        'eight':8,
        'nine':9
    }
    return vals[n] if n in vals else n


lines = [line for line in sys.stdin]
inp1 = [list(map(int, re.findall(r'\d', line))) for line in lines]
inp2 = [list(map(int, map(wordToDigit, re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)))) for line in lines]
def solve(inp):
    return reduce(add, [ls[0]*10 + ls[-1] for ls in inp])

print(solve(inp1))
print(solve(inp2))
