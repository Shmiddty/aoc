import sys
import re
from func import pipe, curry, callWith, ffs
from string import lower
from maths import add

# is this cheating? this feels like cheating
class Unit(str):
    def __radd__(self, other):
        if other == '': return self

        lst = other[-1]
        fst = self[0]
        if lst.lower() == fst.lower() and lst != fst:
            return other[:-1] + self[1:]

        return str.__add__(other, self)

    def __add__(self, other):
        lst = self[-1]
        fst = other[0]
        if lst.lower() == fst.lower() and lst != fst:
            return self[:-1] + other[1:]

        return str.__add__(self, other)

polymer = sys.stdin.read().strip()
print(pipe(
    ffs(
        pipe(
            curry(map, Unit),
            curry(reduce, add),
            len
        ),
        pipe(
            lower,
            set,
            curry(map, pipe(
                curry(re.sub, flags=re.IGNORECASE),

                #             vvvvvvv
                callWith(r'', polymer), # how would you get this from the pipeline
                #             ^^^^^^^   # instead of a variable?

                curry(map, Unit),
                curry(reduce, add),
                len
            )),
            min
        )
    ),

    curry(map, str), '\n'.join
)(polymer))

