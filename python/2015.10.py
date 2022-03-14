import sys
from enum import partition
from func import repeat

inp = sys.stdin.read().strip()

def lookAndSay(seq):
    return reduce(lambda o, ls: o + str(len(ls)) + ls[0], partition(seq), '')

def part1():
    return len(repeat(lookAndSay, inp)(40))

v = part1()
print(v)

def spelunkAndSay(seq, N = 50):
    cache = {}
    def delve(S, d = N):
        k = (S, d)

        if k in cache:
            return cache[k]

        if d < 0: return len(S)
        
        nxt = lookAndSay(S)

        # this approach doesn't work because it doesn't recombine subsequences.
        # that is 12 gets split into [1], [2] which becomes [1,1], [1,2]
        # which should be combined into [1,1,1], [2]
        cache[k] = sum(map(lambda s: delve(''.join(s), d - 1), partition(nxt))) 

        return cache[k]

    return delve(seq)

# I suspect this won't finish, or will be very slow.
# suspicion confirmed. Is it a memory issue?
def part2(N = 50):
    return len(repeat(lookAndSay, inp)(N))
    #return spelunkAndSay(inp, N)
    
    # this doesn't actually work. womp womp
    # that's because the constant approximates the next *value* not the length, you dummy.
    #global v
    #for _ in range(10):
    #    v = v * 1.303577269

    #return int(v)

