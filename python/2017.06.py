import sys
import re
from enum import takeWhile
from func import iterate

inp = map(int, re.findall(r'\d+', sys.stdin.read()))

def takeUntilRepeats(enum):
    out = []
    for v in enum:
        # how efficient is this?
        # will we need to make a dictionary/hash?
        if v in out: break
        out.append(v)
    return out

def step(banks):
    L = len(banks)
    maxVal = max(banks)
    maxIndex = banks.index(maxVal)
    return map(
        lambda (i, v): maxVal / L + (i != maxIndex) * v + ((i + L - maxIndex - 1) % L < maxVal % L),
        enumerate(banks)
    )

steps = takeUntilRepeats(iterate(step, inp))
print(len(steps))

print(len(takeUntilRepeats(iterate(step, step(steps[-1])))))

# L = 4
# maxVal = 7
# maxIndex = 2
# L - maxIndex - 1 = 1
# maxVal % L = 3
# maxVal / L = 1
# 0 1 2 3
# 1 2 3 0 
# 0 2 7 0
# i == 3, 0  + ((6 - 3) % L < 7 == 1) + 1 == 2
# i == 0, 0  + ((6 - 0) % L < 7 == 1) + 1 == 2
# i == 1, 0  + ((6 - 1) % L < 7 == 1) + 1 == 2
# i == 2, 0  + ((6 - 2) % L < 7 == 1) + 1 == 2
