import sys
import re

from region import intersection, size

def toRegion((_, x, y, w, h)):
    return ((x,y), (x+w, y+h))

# (id, x, y, w, h)
claims = [map(int, re.findall(r'\d+', line)) for line in sys.stdin]

# borrowing from the future!
#def boot(ls):
#    return reduce(lambda A, b: A + [(-1, b)] + inter(A, b), ls, [])
#
#def inter(A, b):
#    return filter(lambda (_,r): r != None, map(lambda (s, a): (-1 * s, intersection(a, b)), A))
#
## Part 1
#regions = map(toRegion, claims)
#print(sum(map(lambda (s, r): s * size(r), boot(regions))))
## wrong!

#def intersecting(ls):
#    return [a
#        for a in ls
#        for b in ls
#        if a != b and intersection(toRegion(a), toRegion(b)) != None
#    ]

# Part 1
#print(sum(map(lambda (i, x, y, w, h): w * h, intersecting(claims))))
## wrong!

# Part 1
def claim(paper, (i, X, Y, w, h)):
    for y in range(h):
        for x in range(w):
            paper[(Y+y)*1000 + X + x] += 1
    
    return paper

claimed = reduce(claim, claims, [0]*(1000**2))
print(len(filter(lambda v: v > 1, claimed)))
# I half expected a million item list to run into memory issues, but this worked just fine. 
# I was overcomplicating things with this one because the solutions to seemingly similar problems
# influenced my approach to it. Almost like some kind of bias. hmmmmmmmmmmmmmmmmmm...
# The effort wasn't totally wasted, but I did end up spinning my wheels for a bit because of it.

# Part 2
def firstUniqueClaim(claims):
    for a in claims:
        uniq = True
        for b in claims:
            if a == b: continue
            if intersection(toRegion(a), toRegion(b)) != None:
                uniq = False
                break
        if uniq: return a 

    return None

print(firstUniqueClaim(claims)[0])
