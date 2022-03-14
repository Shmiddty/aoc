import sys

from enum import aggregate, combinations, nth
from func import memo

magg = memo(aggregate) # this is overkill and unnecessary

def dlist(d):
    return map(lambda k: (k, d[k]), d)

def hasAnyN(N = 2):
    return lambda word: any(map(
        lambda (k, n): n == N,
        dlist(magg(word))
    ))

words = [line.strip() for line in sys.stdin]

# Part 1
twos = filter(hasAnyN(2), words)
threes = filter(hasAnyN(3), words)
print(len(twos) * len(threes))

# Part 2
def intersection((a, b)):
    return set(enumerate(a)) & set(enumerate(b))

mostestOverlappingest = sorted(map(intersection, combinations(words, 2)), key=len).pop()
print(''.join(map(nth(1), sorted(mostestOverlappingest, key=nth(0)))))
