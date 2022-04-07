import sys

inp = [line.strip() for line in sys.stdin]

# Part 1
print(sum(map(lambda a: len(a) - len(eval(a)), inp)))

# Part 2
#print(sum(map(lambda a: 2 + len(filter(lambda c: c in "\\\"", a)), inp)))
print(sum(map(lambda a: 2 + sum([1 for c in a if c in "\\\""]), inp)))

