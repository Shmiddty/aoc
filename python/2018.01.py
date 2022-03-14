import sys
from itertools import takewhile, cycle

init = [int(line) for line in sys.stdin]

# part 1
print(sum(init))

# how would I do this functionally?
def untilrepeats(deltas = cycle(init)):
    freq = 0
    freqs = {}
    while freq not in freqs:
        freqs[freq] = 1
        freq += next(deltas)

    return freq

print(untilrepeats())
