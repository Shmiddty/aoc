import sys
from itertools import groupby, count, dropwhile
from math import sqrt, ceil
from functools import partial

from string import digits
from enum import chunk, combinations, flatten, uniq, nth, aggregate
from vector import diff, add, mul, scale, dot, magnitude, inverse, vsqrt
from func import curry, pipe, less, iterate, iterN, over, callWith, spread
from grid import manhattan

manh = curry(manhattan, (0,0,0))

particles = [(i, tuple(map(tuple, chunk(digits(line), 3)))) for (i, line) in enumerate(sys.stdin)]

# part 1
print(
    min( # find the lowest
        particles, # in particles
        key=lambda (i,(p,v,a)): manh(a) # by acceleration
    )[0] # get the index
)

# possible solution for part 2
# find all combinations of particles
# for each combination add those particles to collision set if the particles ever collide
# remove the collision set from the set of all particles 

# use an empty tuple to represent all points?
Infinity = sys.maxint 
def quadratic(a, b, c):
    if a == 0: # this is acutally a linear equation, you scoundrel! 
        return (
            None, 
            -c / b if b != 0 else (
                None if c != 0 else Infinity
            )
        )

    left = -b / 2 / a
    s = b*b - 4 * a * c
   
    # this is wrong-ish, should be a complex number
    if s < 0: return None, None

    right = sqrt(s) / 2 / a
    return left - right, left + right

# this should be the correct approach, I just need to figure out the math behind it
def collidesAt((ap, av, aa), (bp, bv, ba)):
    # p(t) = p0 + v0*t + a0*(t * (t+1) / 2) 
    # ap + av*t + aa * (t * (t+1) / 2) = bp + bv*t + ba * (t * (t+1) / 2)
    # 0 = (bp - ap) + (bv - av) * t   +   (ba - aa)/2 * t + (ba - aa)/2 * t**2 

    dp = diff(bp, ap)
    dv = diff(bv, av)
    da = diff(ba, aa)
    
    # 0 = da/2 * t**2 + (dv + da/2) * t + dp
    a = scale(.5, da)
    b = add(dv, a)
    c = dp

    # they're colliding now!
    #if magnitude(dp) == 0: return None, 0
    
    # t = (ap - bp) / (bv - av)
    #if magnitude(da) == 0: return dot(diff(ap, bp), inverse(dv))

    # just do the quadratic equation for each dimension. duh.
    times = map(spread(quadratic), zip(a,b,c))

    # this migth be wrong? 
    if all(map(lambda tp: Infinity in tp, times)):
        return 0

    # the time must be the same in each dimension or there is no collision
    possible = filter(
        lambda t: t != Infinity and t != None and all(map(
            # Infinity represents intersecting parallel lines
            lambda tp: t in tp or Infinity in tp, 
            times
        )), 
        flatten(map(list, times))
    )

    if len(possible) == 0: return None

    return possible[0]

    #t = set(filter(lambda t: t != Infinity, times))
    #print(t) 
    #return t if len(t) == 1 else None
    #for t in times[0]: # what if t == Infinity?
    #    if all(map(lambda tp: t in tp or Infinity in tp, times[1:])):
    #        return t
    #        
    #return None

    ## these need to be ints, should I ceil, float, or trunc?
    #itimes = map(int, filter(bool, flatten(map(list, times))))
    ##print(itimes)
    #if not len(itimes): return None

    #counts = aggregate(itimes)
    #mostkey = max(counts, key=counts.get)
    #mostval = counts[mostkey]

    ##print(mostkey, mostval)

    #if mostval == len(ap): return mostkey
    #return None

    # [-, -, -], [+, +, +] 
    #minus, plus = zip(*times)
    #print(minus, plus)

    #return (
    #    minus[0] if len(set(minus)) == 1 else None, 
    #    plus[0] if len(set(plus)) == 1 else None
    #)
  
    # Beyond here lie the scribblings of a madman


    ## t = (-(dv + da/2) +/- sqrt((dv + da/2)**2 - 4 * (da/2) * dp)) / (2da)
    ## t = -(1/2 * (dv/da) + 1/4) +/- sqrt((dv + da/2)**2 - 2*da*dp)/(2da)
    #
    #dp = bp - ap
    #dv = bv - av
    #da = ba - aa
    #t = -(1/2 * (dv/da) + 1/4) + ((dv + da/2)**2 - 2*da*dp)**(1/2) * 1/(2*da)

    #return t

    #a = scale(0.5, da)
    #b = add(dv, scale(0.5, da))
    #c = dp
    #i2c = inverse(scale(2, c))
    #l = -dot(i2c, b)
    #r = dot(i2c, sqrt(magnitude(b)**2 - dot(scale(4, a), c))))

    #if r < 0: return None

    #return l + r

    ## sqrt(vector) = scale(sqrt(mag(vector)), vector)

    ## the sqrt of a vector times a vector should be a vector?

    ## 0 = da/2*t**2 + da/2*t
    ## t = ((da/2) +/- sqrt((da/2)**2 - 4(da/2)*0)) / (2da)
    ## t = -da/2/(2da) (2.0, 0, 1), (2.0, 1, 2),+/- sqrt(da**2 / 4 - 2 * da * 0) / (2da)
    ## t = -.25 +/ da/2 / 2da 
    ## t = -.25 +/- .25

    ## ap - bp + av - bv = (ba - aa) * (t * (t+1) / 2)
    ## da = ba - aa, dv = bv - av, dp = bp - ap
    ## 0 = da * (.5t**2 + .5t) + dp + dv * t 
    ## 0 = .5*da*t**2 + .5*da*t + dp + dv * t
    ## 0 = (.5*da)*t**2 + (.5 * da + dv) * t + dp
    ## a = .5 * da, b = .5 * da + dv, c = dp

    ## t = (-b +/- sqrt(b**2 - 4*a*c)) / 2 / a
    ## t = -(.5da + dv) / 2 / .5da +/- sqrt(...) / 2 / .5da
    ## t = -(1 + dv / .5da) / 2 ...
    ## t = -.5 - dv / da +/- sqrt((.5da)**2 - 4(.5da)(dp)) / 2da

    ## I need a better grasp on vector math
  
    ## this is obviously wrong. Things can collide without having acceleration
    ##if magnitude(da) == 0: return None
    ##if magnitude(da) == 0: return None, None
    #
    #ida = inverse(da)
    #
    #a = scale(.5, da)
    #b = add(scale(.5, da), dv)
    #c = dp

    ## not sure if this is correct. 
    #s = magnitude(b) - 4 * dot(a, c)
    ## this might also be wrong
    #s = dot(b, b) - 4 * dot(a, c)

    #if s < 0: return None
    ##if s < 0: return None, None
    #
    #sqrts = sqrt(s)
    ##twoA = scale(2, a)
    ## 
    #dvDda = dot(dv, ida)
    #sqrtsD2da = magnitude(scale(sqrts, scale(2, ida)))
    ## sqrts / twoA  is... the inverse of twoA scaled by sqrts
    #print(sqrts, dvDda, sqrtsD2da) 
    #return -.5 - dvDda + sqrtsD2da
    ##return -.5 - dvDda - sqrtsD2da, -.5 - dvDda + sqrtsD2da

    ##return (-b + sqrts) / twoA, (-b - sqrts) / twoA

def willCollide(arg):
    return collidesAt(arg) > 0
    minus, plus = collidesAt(arg)
    return plus > 0 or minus > 0
    #ta, tb = collidesAt(arg)
    #if ta >= 0 or tb >= 0: print(ta, tb)
    #return ta >= 0 or tb >= 0

def prune(byt):
    _, cols = byt[0]
    remove = set(flatten(cols))
    # this feels so icky
    return remove, filter(lambda (t, cols): len(set(flatten(cols)) | remove) > 0 , byt)

def resolveCollisions(parts):
    pairs = combinations(parts, 2)
    collisions = sorted(filter(
        lambda (t, a, b): t != None,
        map(lambda ((a, av), (b, bv)): ((collidesAt(av, bv)), a, b), pairs)
    ))
    #print("# colls", len(collisions))
    cur = [(t, map(lambda (t, a, b): [a,b], g)) for (t, g) in groupby(collisions, key=nth(0))]
    prev = None

    while prev != cur:
        prev = cur
        remove, cur = prune(cur)
        parts = filter(lambda (i, _): i not in remove, parts)

    return parts

remaining = resolveCollisions(particles)
#print(remaining)
print(len(remaining))

#collided = set(flatten(collisions))
#print(len(collided))

# p(t) = p0 + v0*t + a0*(t * (t+1) / 2) 
def posT(t): return lambda(p,v,a): add(
    add(p, scale(t, v)), 
    scale(t * (t+1) / 2, a)
)

def move((p, v, a)):
    return (add(p, add(v, a)), add(v, a), a)

def step(parts):
    return uniq(map(lambda (i, v): (i, move(v)), parts), key=lambda (i, (p,v,a)):p)

#positions = map(lambda f: map(pipe(nth(1), f), particles), map(posT, range(0, 10000)))

#print(positions[0:5])
#for p in positions[0:5]: print(p)
#uncollided = set(particles).difference(
#    flatten(filter(willCollide, combinations(particles, 2)))
#)

#counter = count(0)
#uncollided = takewhile(
#    pipe(
#        curry(next, counter), 
#        less(10000)
#    ), 
#    iterate(step, particles)
#)
#print([(i, len(next(uncollided))) for i in range(10)])
#steps = iterN(step, 1000)(particles)
#print(map(len, steps))

#timer = count(0)
#
#uncollided = next(dropwhile(
#    lambda ls: any(map(partial(willCollide, next(timer)), combinations(ls, 2))),
#    iterate(step, particles)
#))
#
#print(len(uncollided))
# 574 is too high. I'm guessing there's a pair that collides wayyyyy off into the future
