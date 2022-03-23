from math import sqrt

def isnumber(n):
    return type(n) in [int, float]

# work in progress
class vec:
    def __init__(self, *dims): self._vec = dims
    def __str__(self): return "(%s)"%','.join(map(str,self._vec))
    def __repr__(self): return "vec%s"%str(self)

    def __eq__(self, other):
        if type(self) != type(other): return False

        return self._vec == other._vec

    def __req__(self, other):
        return self.__eq__(other)

    def __add__(self, other):
        return vec(*add(self._vec, other._vec))

    def __sub__(self, other):
        return vec(*diff(self._vec, other._vec))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isnumber(other):
            return vec(*scale(other, self._vec))

        return dot(self._vec, other._vec)

    def __rdiv__(self, other):
        if isnumber(other):
            return vec(*scale(other, inverse(self._vec)))

        return dot(other._vec, inverse(self._vec))
    def __div__(self, other):
        if isnumber(other):
            return vec(*scale(1.0/other, self._vec))

        return dot(inverse(other._vec), self._vec)

    def __pow__(self, other):
        if isnumber(other) and other == 2:
            return self * self + self ^ self

        return self # ???

    def __and__(self, other): return self # ???
    def __or__(self, other): return self  # ???
    def __xor__(self, other):
        if self == other: return 0 # if they are parallel, really

        # is the dot product of two vectors the magnitude of their bivector?
        return self #??? this should be a kvec?

    def unit(self):
        return vec(*unit(self._vec))

def add(a, b):
    return tuple(map(lambda (A,B): A+B, zip(a,b)))

def diff(a, b):
    return add(a, scale(-1, b))

def mul(a, b):
    return tuple(map(lambda (A,B): A*B, zip(a,b)))

def vsqrt(a):
    return scale(sqrt(magnitude(a)), a)

def inverse(a):
    mag = magnitude(a)
    if mag == 0: return a # a is the origin vector

    return scale((1.0/mag)**2, a)

def dot(a, b):
    return sum(mul(a, b))

def scale(s, a):
    return tuple(map(lambda A: s*A, a))

def magsquared(a):
    return sum(mul(a, a))

def magnitude(a):
    return sqrt(magsquared(a))

def unit(a):
    return scale(1.0 / magnitude(a), a)


