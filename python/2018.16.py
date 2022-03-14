import sys
import re
from enum import chunk, nth, replaceAt
from func import pipe, prtl, fBa, swap, ppmap, spread, nequals, fABfab, I, fall, more, ffs
from string import digits, tokens

parse = pipe(
    prtl(tokens, delimeter='\n\n\n\n'),
    spread(fABfab(
        pipe(
            prtl(tokens, delimeter='\n\n'),
            ppmap(pipe(
                prtl(tokens, delimeter='\n'),
                ppmap(digits),
                ffs(nth(1), ffs(nth(0), nth(2)))
                # [ before, op, after ] -> (op, (before, after))
                # technically unnecessary but is more comfortable
            )),
        ),
        pipe(
            prtl(tokens, delimeter='\n'),
            ppmap(digits)
        )
    ))
)

samples, program = parse(sys.stdin.read().strip())

def checksample((opcode, a, b, c), (before, after)):
    o = []
    C = after[c]
    A = before[a]
    B = before[b]

    if C == A + B: o +=     ['addr']
    if C == A + b: o +=     ['addi']
    if C == A * B: o +=     ['mulr']
    if C == A * b: o +=     ['muli']
    if C == A & B: o +=     ['banr']
    if C == A & b: o +=     ['bani']
    if C == A | B: o +=     ['borr']
    if C == A | b: o +=     ['bori']
    if C == (a > B): o +=   ['gtir']
    if C == (A > b): o +=   ['gtri']
    if C == (A > B): o +=   ['gtrr']
    if C == (a == B): o +=  ['eqir']
    if C == (A == b): o +=  ['eqri']
    if C == (A == B): o +=  ['eqrr']
    if C == A: o +=         ['setr']
    if C == a: o +=         ['seti']

    return opcode, o

def reveng(potentialities):
    ops = []

    pots = sorted(potentialities, key=pipe(nth(1), len))
    while len(pots):
        code, pops = pots.pop(0)
        if len(pops) == 1:
            op = pops[0]
            ops.append((code, op))
            pots = pipe(
                prtl(filter, pipe(nth(0), nequals(code))),
                ppmap(spread(fABfab(I, prtl(filter, nequals(op))))),
                prtl(sorted, key=pipe(nth(1), len))
            )(pots)

    return ops

potential = map(spread(checksample), samples)

print(len(filter(pipe(nth(1), len, more(2)), potential)))

opfns = {
    'addr':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] + reg[b]) ,
    'addi':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] + b) ,
    'mulr':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] * reg[b]) ,
    'muli':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] * b) ,
    'banr':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] & reg[b]) ,
    'bani':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] & b) ,
    'borr':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] | reg[b]) ,
    'bori':lambda reg, (a, b, c):replaceAt(reg, c, reg[a] | b) ,
    'gtir':lambda reg, (a, b, c):replaceAt(reg, c, int(a > reg[b])) ,
    'gtri':lambda reg, (a, b, c):replaceAt(reg, c, int(reg[a] > b)) ,
    'gtrr':lambda reg, (a, b, c):replaceAt(reg, c, int(reg[a] > reg[b])) ,
    'eqir':lambda reg, (a, b, c):replaceAt(reg, c, int(a == reg[b])) ,
    'eqri':lambda reg, (a, b, c):replaceAt(reg, c, int(reg[a] == b)) ,
    'eqrr':lambda reg, (a, b, c):replaceAt(reg, c, int(reg[a] == reg[b])) ,
    'setr':lambda reg, (a, b, c):replaceAt(reg, c, reg[a]) ,
    'seti':lambda reg, (a, b, c):replaceAt(reg, c, a) ,
}
ops = dict(map(spread(fABfab(I, opfns.get)), reveng(potential)))

print(reduce(
    lambda reg, op: ops[op[0]](reg, op[1:]),
    program,
    [0,0,0,0]
)[0])
