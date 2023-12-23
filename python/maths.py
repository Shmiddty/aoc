from functools import reduce

def product(enum):
    return reduce(lambda p, v: p * v, enum, 1)

def add(a, b): return a + b

# changing this probably breaks something
def fadd(n): return lambda b: b + n

def minmax(ls, key=lambda I:I):
    return (min(ls, key=key), max(ls, key=key))

def quadratic(a,b,c):
    return (-b - sqrt(b**2 - 4*a*c)) / 2.0 / a, (-b + sqrt(b**2 - 4*a*c)) / 2.0 / a

# adapted from
# https://www.tutorialspoint.com/euclidean-algorithm-for-calculating-gcd-in-javascript
def gcd(a, b):
    if a == b or b == 0: return a 
    if a == 0: return b
    return gcd(a - b, b) if a > b else gcd(a, b - a)
