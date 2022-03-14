import sys
from enum import aggregate, combinations
from func import fand, memo

inp = [line.strip().split(' ') for line in sys.stdin]

def hasNoDuplicates(ls): return len(ls) == len(set(ls))

print(len(filter(hasNoDuplicates, inp)))

def isAnagram((a, b)): return aggregate(a) == aggregate(b)
def hasNoAnagrams(ls): return not any(map(isAnagram, combinations(ls, 2)))

print(len(filter(fand(hasNoDuplicates, hasNoAnagrams), inp)))
