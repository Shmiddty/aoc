import sys
from collections import deque
from itertools import count, groupby

from func import curry, iterN, pipe, call
from enum import irange

def step(n, v, i):
    v.rotate(-n)
    v.append(i)
    return v

N = int(sys.stdin.read())

buff = reduce(
    curry(step, N),
    range(1, 2018),
    deque([0])
)
print(buff[0])

# for part 2, we should probably use our mathy brain
# but, just for fun, let's try to run this 50 million times

#buff = reduce(
#    curry(step, N),
#    range(1, 50*10**6 + 1),
#    deque([0])
#)
#print(buff[list(buff).index(0) + 1])

# it actually finishes, albeit after about a minute. *shrug*

# The below commented code is investigatory work
#def afterzero(dq):
#    return dq[(list(dq).index(0) + 1) % len(dq)]
#
#buffs = iterN(
#    pipe(
#        deque,                              # shallow-clone into a new deque, since we're mutating
#        curry(step, N),                     # shove the deque into a curried stepper
#        curry(pipe, curry(next, count(1))), # pipe the next value into the stepper
#        call                                # then call the pipe, resolving the stepper
#    ), 
#    10000                                   # do this 10,000 times
#)([0])                                      # and start with a list containing only 0
#
## count the occurrences of the value following 0
#occurs = [(v, len(list(g))) for (v,g) in groupby(map(afterzero, buffs))]
#print(occurs)

# And this is the result of the investigation:
# [(0, 1), (1, 6), (7, 30), (37, 19), (56, 41), (97, 135), (232, 11), (243, 3151), (3394, 1534), (4928, 1883), (6811, 1308), (8119, 1619), ...]
# (numAfterZero, repeatedNTimes) 
# n(k) = n(k-1) + r(k-1)
# r(k) = ?  
# the number following zero is the previous number plus the number of times it was repeated

def thingy(stepsize, initial, iterations):
    out = cur = initial
    for i in irange(1, iterations):
        cur = (cur + stepsize) % i + 1
        out = i if cur == 1 else out
    return out

# faster part 2
print(thingy(N, 0, 50 * 10**6))
