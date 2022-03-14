from enum import flatten
from math import sqrt

def groot(geo):
    # are these just wrong?
    if geo == 0:
        return basis(3)                     # k
    if geo > 0:
        return sqrt(geo) * basis(2)         # j
    if geo < 0:
        return sqrt(abs(geo)) * basis(1)    # i

    # TODO
    if isinstance(geo, basis):              # what is the geometric root of a basis vector?
        0                                   # sqrt(i) == -1?

    if isinstance(geo, kvector):            # ???
        0

    if isinstance(geo, polynomial):             # complete the square?
        0

def isnumber(val):
    return type(val) in [int, float]

def combinelike(terms):
    T = sorted(terms, key=lambda t: t if isnumber(t) else t.ordinal)
    out = [T.pop(0)]
    while len(T):
        cur = T.pop(0)
        prev = out[-1]
        if isnumber(cur) or (not isnumber(prev) and cur.ordinal == prev.ordinal):
            out[-1] += cur
        else:
            out.append(cur)
   
    return filter(bool, out)

def simplify(kvec):
    bases = kvec.bases
    sord = sorted(bases, key=lambda b: b.ordinal)
    sign = sum(map(
        lambda (a,b): abs(bases.index(b) - bases.index(a)),
        zip(bases, sord)
    )) / 2 % 2
    sign = sign * -2 + 1

    scale = sign * kvec.scale 
    # this is wrong, but shouldn't be a problem for the expected use case
    sord = filter(lambda b: sord.count(b) == 1, sord)
   
    # there's some inconsistency in that i is related to rotation
    # because i*i == 1 insead of -1
    # how should this be reconsiled when using arbitrary basis vectors?

    if len(sord) == 1: return scale * sord[0]
    if len(sord) == 0: return scale

    return scale * kvector(*sord)

# TODO: do I need to implement the dot and wedge products?
# TODO: find an elegant way to simplify the products of kvectors
class geometric:
    # addition is commutative
    def __radd__(self, other): return self.__add__(other)
    def __add__(self, other):
        if isinstance(self, basis) and isinstance(other, basis) and self.ordinal == other.ordinal:
            if self.scale + other.scale == 0: return 0

            return basis(self.ordinal, self.scale + other.scale)

        if isinstance(self, kvector) and isinstance(other, kvector) and self.ordinal == other.ordinal:
            return (self.scale + other.scale) * kvector(*self.bases)
     
        if isinstance(self, polynomial) and isinstance(other, polynomial):
            return polynomial(combinelike(self.terms + other.terms))

        if isinstance(self, polynomial):
            return polynomial(combinelike(self.terms + [other])) 
        
        if isinstance(other, polynomial):
            return polynomial(combinelike(other.terms + [self])) 
       
        return polynomial(self, other)
   
    def __neg__(self): return -1 * self
    def __rsub__(self, other): return other + -self 
    def __sub__(self, other): return self + -other

    # implicitly converting to floating point numbers might be undesirable 
    def __rdiv__(self, other):
        return 1.0 / (self * self) * other * self

    def __div__(self, other):
        if isnumber(other):
            return 1.0 / other * self

        return 1.0 / (other * other) * self * other

    def __pow__(self, other):
        if type(other) == int:
            return reduce(lambda o, _: o * self, range(other), 1)

        if type(other) == float: # how to do fractional exponents?
            0 

        return 0 # what does it mean to raise a basis vector to the power of a basis vector?

    # products are not necessarily commutative
    def __rmul__(self, other):
        if other == 0: return 0
        if other == 1: return self
 
        if isinstance(self, polynomial) and isinstance(other, polynomial):
            return sum(combinelike([o * a for o in other.terms for a in self.terms]))

        if isinstance(self, polynomial):
            return sum(combinelike([other * a for a in self.terms]))

        if isinstance(other, polynomial):
            return sum(combinelike([o * self for o in other.terms]))

        if isinstance(self, kvector) and isnumber(other):
            return kvector(other * self.bases[0], *self.bases[1:]) 

        if isinstance(self, basis) and isnumber(other):
            return basis(self.ordinal, self.scale * other) 

        return simplify(kvector(other, self))

    def __mul__(self, other):
        if other == 0: return 0
        if other == 1: return self
       
        if isinstance(self, polynomial) and isinstance(other, polynomial):
            return sum(combinelike([a * o for o in other.terms for a in self.terms]))

        if isinstance(self, polynomial):
            return sum(combinelike([a * other for a in self.terms]))

        if isinstance(other, polynomial):
            return sum(combinelike([self * o for o in other.terms]))

        if isinstance(self, kvector) and isnumber(other):
            return kvector(other * self.bases[0], *self.bases[1:]) 

        if isinstance(self, basis) and isnumber(other):
            return basis(self.ordinal, self.scale * other) 

        return simplify(kvector(self, other))


class basis(geometric):
    def __init__(self, ordinal = 1, scale = 1):
        self.ordinal = ordinal
        self.scale = scale

    def __req__(self, other): return self.__eq__(other)
    def __eq__(self, other):
        if not isinstance(other, basis): return False

        return self.ordinal == other.ordinal and self.scale == other.scale

    def __repr__(self):
        return "basis(%s,%d)"%(str(self.ordinal), self.scale)

    def __str__(self):
        return "%se_%s"%(
            '' if self.scale == 1 else '-' if self.scale == -1 else str(self.scale) + '*',
            str(self.ordinal)
        )

class kvector(geometric):
    def __init__(self, *bases):
        _bases = flatten(map(lambda b: list(b.bases) if isinstance(b, kvector) else b, bases))
        self.scale = reduce(lambda o, b: o * b.scale, _bases, 1)
        self.ordinal = tuple(map(lambda b: b.ordinal, _bases))
        self.bases = map(lambda b: basis(b), self.ordinal)

    def __req__(self, other): return self.__eq__(other)
    def __eq__(self, other):
        if not isinstance(other, kvector): return False

        return self.bases == other.bases and self.scale == other.scale

    def __repr__(self):
        return "kvector(%s%s)"%(
            '' if self.scale == 1 else '-' if self.scale == -1 else str(self.scale) + '*',
            ','.join(map(repr, self.bases))
        )

    def __str__(self):
        return "%se_%s"%(
            '' if self.scale == 1 else '-' if self.scale == -1 else str(self.scale) + '*',
            '_'.join(map(lambda b: str(b.ordinal), self.bases))
        )

class polynomial(geometric):
    def __init__(self, *terms):
        self.terms = flatten(map(
            lambda t: t.terms if isinstance(t, polynomial) else t, 
            terms
        ))

    def __req__(self, other): return self.__eq__(other)
    def __eq__(self, other):
        if not isinstance(other, polynomial): return False
        if len(self.terms) != len(other.terms): return False

        return all(map(lambda (a,b): a==b, zip(self.terms, other.terms)))

    def __repr__(self):
        return "polynomial(%s)"%','.join(map(repr, self.terms))

    def __str__(self):
        return ' + '.join(map(str, self.terms))

# global convenience values
i = e1 = basis(1) # should i be special in that i*i = -1?
j = e2 = basis(2)
k = e3 = basis(3)
