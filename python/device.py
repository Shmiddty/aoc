import sys
from enum import replaceAt, decapitate, nth
from string import digits, tokens
from func import pipe, prtl, spread, fABfab, I

# this is a bespoke parser that assumes the first line is an instruction pointer.
# that is to say... it's wrong.
parse = pipe(
    prtl(tokens, delimeter='\n'),
    decapitate,
    spread(fABfab(
        pipe(digits, nth(0)),
        prtl(map, pipe(
            prtl(tokens, delimeter=' '),
            decapitate,
            spread(fABfab(I, prtl(map, int)))
        ))
    ))
)

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

def run(program, reg = [0,0,0,0], iptr = None):
    if iptr != None: reg += [0, 0]

    i = 0#reg[iptr]
    ptrs = range(len(program))

    while i in ptrs:
        op, args = program[i]
        if iptr != None: reg[iptr] = i
        reg = opfns[op](reg, args)
        if iptr != None: i = reg[iptr]
        i += 1

    return reg


