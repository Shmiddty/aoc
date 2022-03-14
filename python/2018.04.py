import sys
import re
from functools import partial
from itertools import izip_longest as zipl, chain

from enum import partition, nth, chunk, flatten, decapitate, head, tail, take
from func import pipe, curry, callWith, equals, spread
from maths import product

first = nth(0)
second = nth(1)
last = nth(-1)

# what should this be called? Pivot? it's a group-by but with a value mapping
def mapGroupBy(ls, key=lambda en: en[0], val=lambda en: en[1:]):
    # No mutations, but lots of wasted work. Worth it?
    return {
        K: [val(item) for item in ls if key(item) == K]
        for K in set(map(key, ls))
    }
    #out = {}
    #for item in ls:
    #   k = key(item)
    #   if k not in out: out[k] = []
    #   out[k].append(val(item))
    #return out

def mapgroup(ls, key=lambda en: en[0], val=lambda en: en[1:]):
    return [
        (K, [val(item) for item in ls if key(item) == K])
        for K in set(map(key, ls))
    ]

def robosnek(fn): return lambda ls: ls[0:1] + fn(ls[1:])
def concat(ls, val): return ls + (val if type(val) == list else [val])
def add(a,b): return a + b
def eadd(a, b): return map(spread(add), zipl(a, b, fillvalue=0))

def diff(a, b): return b-a
def repeat(a, b): return [a]*b
def swap(a, b): return b, a
def I(a):return a
me = I

def dI(a):
    print(a)
    return a

# f A b = A(b)
def fAb(A, b): return A(b)
call = fAb

# f a B = a, B(a)
def faBa(a, B): return a, B(a)
fabalous = faBa

# f A B = f a b = A(a), B(b)
def fABfab(A, B): return lambda a, b: (A(a), B(b))

# f [A0, ..., An] = f b = [A0(b), ..., An(b)]
def ffs(*F): return lambda *v: map(callWith(*v), F)

inp = [line.strip() for line in sys.stdin]

logs = sorted(inp)

# [[YYYY, MM, DD, hh, mm, ?id?], ...]
nlogs = map(
    #lambda log: map(int, re.findall(r'\d+', log))
    pipe(
        curry(re.findall, r'\d+'),
        curry(map, int)
    ),
    logs
)

# [id, sleep, wake, sleep, wake, ...]
shifts = map(
    #lambda ls: ls[-1],
    curry(map, nth(-1)),
    partition(
        nlogs,
        lambda a, b: len(b) == 5 # guard entries are len 6
    )
)

# [id, minutesSlept]
zzzs = map(
    #lambda ls: ls[0:1] + [sum(map(
    #    lambda (i, v): (i%2 * 2 - 1) * v),
    #    enumerate(ls[1:]))
    #],
    robosnek(pipe(
        enumerate,
        curry(map, lambda (i, v): (i%2 * 2 - 1) * v),
        sum,
        curry(concat, [])
    )),
    shifts
)

zzzaggregates = mapGroupBy(zzzs)

# for those hard to reach argument positions
# pipe(curry(A), callWith(B))(C) -> A(C, B)
# pipe(curry(tuple, B), spread(swap), spread(A))(C)

# just imagine if the functor (I always feel like I'm using this word incorrectly)
# for map came after the list. what a headache!
# (keyword arguments are basically cheating)


totalZs = map(
    #lambda k: (k, sum(flatten(zzzaggregates[k]))),
    pipe(
        curry(curry, fabalous), # curry. curry fabalous.
        callWith(
            pipe(
                zzzaggregates.get,
                flatten,
                sum
            )
        )
    ),
    zzzaggregates
)

sleepiestid, minutesslept = max(totalZs, key=nth(1))
sleepyshifts = filter(pipe(nth(0), equals(sleepiestid)), shifts)
sleepyschedule = flatten(map(
    pipe(
        tail,
        curry(chunk),
        callWith(2), # [(a0, b0), ..., (aN, bN)]
        curry(map,
            #lambda (a, b): [0]*a + [1]*(b-a)
            pipe(
                curry(fabalous),        # curry. still fabalous
                callWith(spread(diff)), # ((a, b), b-a) not quite what we want...
                spread(swap),           # (b-a, (a, b))
                list,
                flatten,
                take(2),
                spread(swap),           # (a, b-a)
                enumerate,
                curry(map, spread(repeat)),
                spread(concat)
            )
        )
    ),
    sleepyshifts
))

sleepyhistogram = list(enumerate(reduce(
    eadd,
    sleepyschedule,
    repeat(0, 60)
)))

sleepiestminute, sleptcount = max(sleepyhistogram, key=nth(1))

# Part 1 solution
#print(sleepiestid * sleepiestminute)

def hizzztogram(gid):
    return list(enumerate(reduce(
        eadd,
        flatten(map(
            pipe(
                tail,
                curry(chunk),
                callWith(2),
                curry(map,
                    pipe(
                        curry(fabalous),
                        callWith(spread(diff)),
                        spread(swap),
                        list,
                        flatten,
                        take(2),
                        spread(swap),
                        enumerate,
                        curry(map, spread(repeat)),
                        spread(concat)
                    )
                )
            ),
            filter(pipe(nth(0), equals(gid)), shifts)
        )),
        repeat(0, 60)
    )))

# Part 2 - easy-ish-mode
#print(
#    pipe(
#        curry(max, key=pipe(nth(1), nth(1))),
#        list,
#        flatten,
#        take(2),
#        product
#    )(map(
#        pipe(
#            curry(fabalous),
#            callWith(
#                pipe(
#                    hizzztogram,
#                    curry(max, key=nth(1)),
#                    list
#                )
#            )
#        ),
#        set(map(nth(0), shifts))
#    ))
#)

# Part 2 - harder-ish-mode
#print(
#    pipe(
#        curry(max, key=pipe(nth(1), nth(1))),
#        list,
#        flatten,
#        take(2),
#        product
#    )(map(
#        pipe(
#            curry(fabalous),
#            callWith(pipe(
#                curry(equals),
#                curry(pipe, nth(0)),
#                curry(filter),
#                callWith(shifts),
#                curry(map, pipe(
#                    tail,
#                    curry(chunk),
#                    callWith(2),
#                    curry(map, pipe(
#                        curry(fabalous),
#                        callWith(spread(diff)),
#                        spread(swap),
#                        list,
#                        flatten,
#                        take(2),
#                        spread(swap),
#                        enumerate,
#                        curry(map, spread(repeat)),
#                        spread(concat)
#                    ))
#                )),
#                flatten,
#                partial(partial, reduce, eadd),
#                callWith(repeat(0, 60)),
#                enumerate,
#                list,
#                curry(max, key=nth(1)),
#                list
#            ))
#        ),
#        set(map(nth(0), shifts))
#    ))
#)
#
## Part 2 again - entire pipeline from raw input
#print(pipe(
#    sorted, # we're dealing with ISO-ish datestamped logs, so we can just string sort
#
#    curry(map, pipe(
#        curry(re.findall, r'\d+'),          # pull out all of the digits
#        curry(map, int)                     # and convert them to ints
#    )),
#
#    partial(partial, partition),            # partition the list into shifts
#    callWith(pipe(
#        fABfab(I, I), # args as tuple
#        second, len, equals(5)              # with an entry of length 5 indicating a new shift
#    )),
#
#    curry(map, curry(map, last)),           # grab just the last number from each entry in each partition
#
#    curry(map, pipe(                        # convert the shifts into minute-blocks
#        #punishment for sleeping on duty
#        decapitate,                         # grab the guard's head, and the logs for their shift (tail)
#        spread(fABfab(I, pipe(              # keep the head for later, we're going to process the shift
#            curry(chunk),                   # break the tail into chunks
#            callWith(2),                    # of size 2
#            curry(map, pipe(                # for each chunk, (a, b)
#                curry(faBa),
#                callWith(spread(diff)),     # ((a,b), b-a)
#                spread(fABfab(first, I)),   # (a, b-a)
#                enumerate,                  # [(0, a), (1, b-a)]
#                curry(map, spread(repeat)), # [[0]*a, [1]*(b-a)]
#                spread(concat)              # [0]*a + [1]*(b-a)
#            )),
#            partial(partial, reduce, eadd), # add each processed chunk
#            callWith(repeat(0, 60)),        # into a minute-blocked list filled with zeros
#        ))),
#        list                                # convert the tuple to a list
#    )),
#
#    curry(mapgroup, key=head, val=second),  # group each shift using the guard's head as our key
#
#    curry(map, spread(fABfab(I, pipe(
#        curry(reduce, eadd),                # combine all of the shifts for each guard
#        enumerate,                          # number each minute in the combined shifts
#        curry(max, key=second)              # find the minute they were most-often asleep
#    )))),
#
#    curry(max, key=pipe(second, second)),   # find the guard who slept most often at the same minute
#    spread(fABfab(I, head)),                # we just need the guard id and the minute
#
#    product                                 # multiply those values to get our answer
#)(inp))
#
#print('---')
# Part 1 and 2 in a single pipeline!?
print(pipe(
    sorted,

    curry(map, pipe(
        curry(re.findall, r'\d+'),
        curry(map, int)
    )),

    partial(partial, partition),
    callWith(pipe(
        # since partition expects a lambda with two arguments,
        # this turns the arguments into a tuple. But I don't like it.
        fABfab(me, I),
        second, len, equals(5)
    )),

    curry(map, curry(map, last)),

    curry(map, pipe(
        decapitate,
        spread(fABfab(I, pipe(
            curry(chunk),
            callWith(2),
            curry(map, pipe(
                ffs(first, spread(diff)),
                enumerate,
                curry(map, spread(repeat)),
                spread(chain)
            )),
            partial(partial, reduce, eadd),
            callWith(repeat(0, 60)),
        ))),
        list
    )),

    curry(mapgroup, key=head, val=second),
    curry(map, spread(fABfab(I, curry(reduce, eadd)))),

    # don't put books on the floor in the library.
    # there's poopoo on the ground from people's shoes. duh.

    ffs(
        pipe(
            curry(max, key=pipe(second, sum)),
            spread(fABfab(I, pipe(
                enumerate,
                curry(max, key=second),
                first
            )))
        ),
        pipe(
            curry(map, spread(fABfab(I, pipe(
                enumerate,
                curry(max, key=second)
            )))),
            curry(max, key=pipe(second, second)),
            spread(fABfab(me, first))
        )
    ),

    curry(map, pipe(product, str)),

    '\n'.join
)(inp))
