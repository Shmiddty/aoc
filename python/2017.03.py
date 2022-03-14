import sys
from math import ceil, sqrt
from functools import partial
from func import iterate, less, pipe
from enum import takeWhile, at
from maths import add
from grid import Grid, manhattan
inp = int(sys.stdin.read())

# had to look this up again
def triNum(n): return n * (n + 1) / 2

# 37 36  35  34  33  32 31
# 38 17  16  15  14  13 30
# 39 18   5   4   3  12 29
# 40 19   6   1   2  11 28
# 41 20   7   8   9  10 27
# 42 21  22  23  24  25 26 
# 43 44  45  46  47  48 49 ---> ...
# I think there's a way to do this in constant time. 
# if only I could remember how to do it.
# 1 + 8 = 9 + 16 = 25 + 24 = 49...  ?
# 8*0+1   8*1+1    8*3+1     8*6+1  8*10+1?
# 8*tri(n)+1
# Here's my very icky implementation of i -> x,y
# for a spiral grid
def indexToCoord(i):
    # i = 8 * (n * (n + 1) / 2) + 1 ...  + c
    # (i - 1) / 4 = n**2 + n + 0
    # 0 = n**2 + n + -(i - 1) / 4
    # (and then I applied the quadratic formula)
    # n = (sqrt(i - c) - 1) / 2 
    # the "ring number"
    r = int(ceil(sqrt(i)/2 - 0.5))
    
    # the max value in the ring
    mx = 8 * triNum(r) + 1
    mn = mx - 8 * r + (r > 0)
    mid = mx - 4 * r

    pos = 0 if r == 0 else abs(mid - i) % (r * 2)
    # 0 1 2 3 0
    # 1 0 1 0 1
    # 2 1 0 1 2
    # 3 0 1 0 3
    # 0 1 2 3 0

    rpos = pos - r
    # -2 -1  0  1 -2
    # -1 -1  0 -1 -1
    #  0  0  0  0  0
    #  1 -1  0 -1  1
    # -2 -1  0  1 -2
    
    side = 0 if r == 0 else ((mx - i) / (r * 2) + 1) * (pos > 0)
    # eg:
    # 0 3 3 3 0
    # 2 0 3 0 4
    # 2 2 0 4 4
    # 2 0 1 0 4
    # 0 1 1 1 0

    tb = side % 2 != 0
    lr = side % 2 == 0

    signx = (i < mn + 2*r or i > mx - r) * 2 - 1
    signy = (i < mn + r or i > mx - 3*r) * 2 - 1
    if side == 0: 
        return r * signx, r * signy

    x = lr * r * signx + rpos * tb
    y = tb * r * signy + rpos * lr

    return x, y

print(manhattan((0,0), indexToCoord(inp)))

def part2():
    G = Grid([((0,0), 1)])
    i = 1
    while 1:
        i += 1
        pt = indexToCoord(i)
        n = G.neighbors(pt, True)
        val = sum(map(G.get, n))
        if val > inp: return val
        G.set(pt, val)

# 284098 too high 
# 268962 still too high
print(part2())
