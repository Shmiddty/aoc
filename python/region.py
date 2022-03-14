from maths import product, minmax
from vector import add as vadd, diff
from enum import without, flatten

# Size of a region; Area for 2d, Volume for 3d, etc
def size(region):
    return product(diff(*region))

# return a region that contains all points in the collection
def containing(points):
    return zip(*map(minmax, zip(*points)))

# return all points within a 2d region
# TODO: dimension-agnostic
def points2d(region):
    xs, ys = zip(*region)
    return [(x, y) for x in range(*vadd(xs, (0,1))) for y in range(*vadd(ys, (0,1)))]

# returns the points on the perimeter of a 2d region
# TODO: make this dimension-agnostic
def border2d(region):
    xs, ys = zip(*region)
    return sorted(set(flatten(
        map(lambda x: map(lambda y: (x, y), range(*vadd(ys, (0,1)))), xs) +
        map(lambda y: map(lambda x: (x, y), range(*vadd(xs, (0,1)))), ys)
    )))

# Intersection of two regions
def intersection(one, two):
    if one == None or two == None:
        return None

    (a, b) = one
    (c, d) = two
    mx = tuple(map(min, zip(b,d)))
    mn = tuple(map(max, zip(a,c)))

    return None if any(map(lambda v: v < 0, diff(mx, mn))) else (mn, mx)

