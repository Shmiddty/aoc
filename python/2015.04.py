import sys
import hashlib

inp = [line.strip() for line in sys.stdin][0]

def salty(key, n = 5):
    i = 1
    while True:
        val = hashlib.md5(key + str(i)).hexdigest()
        if str(val)[0:n] == "0" * n:
            return i

        i += 1

def part1(key):
    return salty(key, 5)

print(part1(inp))

# I predict that this will not finish in a reasonable time
# I was wrong.
def part2(key):
    return salty(key, 6)

print(part2(inp))
