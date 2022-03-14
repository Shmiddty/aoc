import sys
from enum import replaceAt, nth, within, takeWhile
from func import iterate, pipe 

inp = [int(line) for line in sys.stdin]

# this is rather slow. probably using too much memory
def step((i, jmps)):
    return (i + jmps[i], replaceAt(jmps, i, jmps[i] + 1))

# so much faster with mutations
def mutstep((i, jmps)):
    jmps[i] += 1
    return (i + jmps[i] - 1, jmps) 

stepper = takeWhile(pipe(nth(0), within(range(len(inp)))))
finp = list(inp) # since we're mutating it, let's make a copy
steps = stepper(iterate(mutstep, (0, finp)))
print(len(steps) - 1)

# this is taking much longer... are we expected to maths this one?
# looks like very probably yes. 
# in the meantime, my lap is getting a bit of warmth, so that's nice.
def mutstep2((i, jmps)):
    delta = (jmps[i] < 3) * 2 - 1
    jmps[i] += delta
    return (i + jmps[i] - delta, jmps) 

sinp = list(inp) # this isn't neccessary, really
steps2 = stepper(iterate(mutstep2, (0, sinp)))
print(len(steps2) - 1)
