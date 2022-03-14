import sys
import re
from enum import permutations, unzip, chunk, flatten

def isValid(sides):
    return all(map(lambda (a, b, c): a + b > c, permutations(sides, 3)))

one = [map(int, re.findall(r'\d+', line)) for line in sys.stdin]
print(len(filter(isValid, one)))

two = flatten(map(unzip, chunk(one, 3)), 1)
print(len(filter(isValid, two)))
