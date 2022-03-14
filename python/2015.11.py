import sys
from enum import at, divvy
from func import pipe, equals

inp = sys.stdin.read().strip()

# should a be 0 or 1?
# we can have multiple leading zeros
alpha = 'abcdefghijklmnopqrstuvwxyz'
def fromStr(s):
    return map(alpha.index, s)

def toStr(ls):
    return ''.join(map(at(alpha), ls))

def increment(ls):
    if len(ls) == 0: return [0]

    last = (ls[-1] + 1) % 26
    if last == 0:
        return increment(ls[0:-1]) + [last]

    return ls[0:-1] + [last]

def hasStraight(ls):
    return any(map(lambda (a,b,c): c - b == 1 and b - a == 1, zip(ls, ls[1:], ls[2:])))

def isAmbiguous(ls):
    return len(set(fromStr('iol')) & set(ls)) > 0

def hasUniqueNonOverlappingPairs(s, n = 1):
    return n <= len(set(map(
        tuple,
        filter(pipe(set, len, equals(1)), divvy(s, 2))
    )))

def isValid(ls):
    return hasStraight(ls) and not isAmbiguous(ls) and hasUniqueNonOverlappingPairs(ls, 2) 

def gen(init = inp):
    cur = fromStr(init)
    while not isValid(cur):
        cur = increment(cur)

    return toStr(cur)

one = gen()
print(one)

two = gen(toStr(increment(fromStr(one))))
print(two)
