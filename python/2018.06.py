import sys
from functools import partial

from enum import nth, flatten, mapgroup
from maths import minmax, add
from func import pipe, curry, spread, callWith, fAb, ffs, I, swap, fABfab, equals, less
from vector import add as vadd
from grid import manhattan

# return the minimum if it is the only minimum else return None
def uniqmin(ls, key=lambda a:a):
    mns = map(key, ls)
    mn = min(mns)
    if mns.count(mn) > 1: return None
    return ls[mns.index(mn)]

#def entuple(a): return (a,)
#def enlist(a): return [a]
#
#def dI(a):
#    print(a)
#    return a
#
#coords = [map(int, line.split(',')) for line in sys.stdin]
#print(pipe(
#    spread(zip),
#    curry(map, pipe(
#        minmax,
#        curry(vadd, (0, 1)),
#        spread(range),
#        curry(map, entuple)
#    )),
#
#    spread(swap),
#    spread(fABfab(
#        pipe(
#            curry(callWith),
#            curry(pipe, curry(add), curry(map))
#        ),
#        I
#    )),
#    spread(map),
#
#    flatten,
#
#    curry(map, ffs(I, pipe(
#        curry(manhattan),
#        curry(uniqmin, coords) # <-- TODO: unwanted variable usage!
#    ))),
#
#    curry(filter, pipe(nth(1), bool)),
#    curry(map, spread(fABfab(I, tuple))),
#    curry(mapgroup, key=nth(1), val=nth(0)),
#
#    curry(filter, pipe(
#        nth(1),
#        pipe(
#            spread(zip),
#            curry(map, minmax),
#
#            # This bit is fun.
#            # given [[minx, maxx], [miny, maxy]]
#            # this provides a list of all points on the perimeter
#            # if I were to generalize it, it should look something like
#            # def border((x0, y0), (x1, y1)):
#            # obviously the function composition would be different in that case
#            ffs(spread(swap), I),
#            curry(map, pipe(
#                spread(fABfab(
#                    pipe(
#                        curry(map, entuple),
#                        curry(callWith),
#                        curry(pipe, curry(add), curry(map))
#                    ),
#                    pipe(
#                        curry(vadd, (0,1)),
#                        spread(range),
#                        curry(map, entuple)
#                    )
#                )),
#                spread(map),
#                flatten
#            )),
#            spread(fABfab(I, curry(map, spread(swap)))),
#            spread(add),
#            set,
#            # end fun bit
#
#            partial(partial, set.intersection)
#        )(coords), # <-- TODO: unwanted variable usage!
#        len,
#        equals(0)
#    )),
#
#    curry(map, spread(fABfab(I, len))),
#    curry(map, nth(1)),
#    max
#)(coords))

# I'm drowning in curry

from region import containing, border2d, points2d
print(pipe(
    ffs(
        pipe(
            ffs(
                pipe(
                    containing,
                    border2d,
                    set,
                    partial(partial, set.intersection),
                    partial(partial, pipe, nth(1)),
                    callWith(len, equals(0)),
                ),
                pipe(
                    ffs(
                        pipe(
                            partial(partial, uniqmin),
                            curry(pipe, curry(manhattan)),
                            partial(ffs, I)
                        ),
                        pipe(containing, points2d)
                    ),
                    spread(map),
                    curry(filter, pipe(nth(1), bool)),
                    curry(mapgroup, key=pipe(nth(1), tuple), val=nth(0)),
                )
            ),
            spread(filter),
            curry(map, spread(fABfab(I, len))),
            curry(map, nth(1)),
            max
        ),
        pipe(
            ffs(
                pipe(
                    curry(callWith),
                    curry(pipe, curry(manhattan), curry(map))
                ),
                pipe(containing, points2d)
            ),
            spread(map),
            curry(map, sum),
            curry(filter, less(10000)),
            len
        )
    ),
    curry(map, str), '\n'.join
)([map(int, line.split(',')) for line in sys.stdin]))

