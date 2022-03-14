import sys
from enum import take, flatten, concat, decapitate, chunk
from func import swap, prtl, pipe, ffs, ppmap, spread, fABfab, fAb, fAB, I, callWith

# the name for this could be better
# maybe... fI?
def discard(fn): return lambda *_: fn()

# You could get with this:
def parseTree(inp):
    return pipe(
        iter,
        ffs(
            pipe(
                prtl(prtl, fAb, parseTree),
                prtl(discard),
                prtl(prtl, map),
            ),
            pipe(next, range),
            pipe(next, take),
            I,
        ),
        prtl(prtl, chunk),
        callWith(2),
        spread(fABfab(spread(fAb), spread(fAb))),
        spread(swap)
    )(inp)

# or you could get with that:
def parseTree(inp):
    np = iter(inp)
    cn, mn = take(2)(np)
    return swap([parseTree(np) for _ in range(cn)], take(mn)(np))

# is this the correct general form?
def traverse(op, (value, children)):
    return reduce(
        pipe(
            fABfab(prtl(prtl, op), prtl(prtl, traverse, op)),
            spread(fAB)
        ),
        children,
        value
    )

# I don't want to rewrite this one at the moment.
def nodevalue((value, children)):
    return sum(map(
        lambda i: nodevalue(children[i - 1]) if i - 1 < len(children) else 0,
        value
    )) if len(children) else sum(value)

print(pipe(
    ppmap(int),
    parseTree,

    ffs(
        pipe(prtl(traverse, concat), sum),
        nodevalue
    ),

    ppmap(str), '\n'.join
)(sys.stdin.read().strip().split(' ')))
