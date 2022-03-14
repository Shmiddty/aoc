import sys
from enum import divvy, within
from func import pipe, equals

inp = [line.strip() for line in sys.stdin]

def numVowels(s):
    return sum(map(s.count, "aeiou")) 

def repeats(s, n = 2):
    return filter(pipe(set, len, equals(1)), divvy(s, n))

def hasRepeat(s, n = 2):
    return len(repeats(s, n)) > 0

def includesAny(s, vals = ["ab", "cd", "pq", "xy"]):
    return any(map(within(s), vals))

def isNice(s):
    return all([not includesAny(s), numVowels(s) > 2, hasRepeat(s)])

def part1(vals):
    return len(filter(isNice, vals))

#print(part1(["ugknbfddgicrmopn"]) == 1)
#print(part1(["aaa"]) == 1)
#print(part1(["jchzalrnumimnmhp"]) == 0)
#print(part1(["haegwjzuvuyypxyu"]) == 0)
#print(part1(["dvszwmarrgswjxmb"]) == 0)

print(part1(inp))

def hasNonOverlappingPair(s):
    pairs = divvy(s, 2)
    for (i, pair) in enumerate(pairs):
        if pair in pairs[i+2:]:
            return True

    return False

def hasChaperonedCouple(s):
    return any([s[i] == s[i+2] for i in range(len(s) - 2)])

def isNicer(s):
    return all([hasNonOverlappingPair(s), hasChaperonedCouple(s)])

def part2(vals):
    return len(filter(isNicer, vals))

#print(part2(["qjhvhtzxzqqjkmpb"]) == 1)
#print(part2(["xxyxx"]) == 1)
#print(part2(["uurcxstgmygtbstg"]) == 0)
#print(part2(["ieodomkazucvgmuy"]) == 0)

print(part2(inp))
