import sys
import re
from enum import nth, uniq

def mols(s):
    return list(re.findall(r'[A-Z][a-z]?', s))

rep, mol  = sys.stdin.read().strip().split('\n\n')
reps = [(a, b) for (a, b) in [tuple(r.split(' => ')) for r in rep.split('\n')]]
mol = mols(mol)
eles = set(map(nth(0), reps)) 

def step(chem):
    return uniq([
        chem[0:i] + mols(r) + chem[i+1:]
        for (i, a) in enumerate(chem) for (b, r) in reps if a == b
    ], key=tuple)

#part1
print(len(step(mol)))

# I'm not sure this will finish.
# yeah... too slow.
def part2():
    cur = [['e']]
    i = 0
    while 1:
        i += 1
        cur = [b for a in cur for b in step(a)]
        if mol in cur:
            return i

#print(part2())
