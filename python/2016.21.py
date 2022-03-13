import sys

sys.path.insert(0, './lib/')
from enum import rotate, without
from func import memo, repeat
from maths import minmax

wo = memo(without)

def parseLine(line):
    parts = line.split(' ')
    op, args = {
        'swap position': lambda a,b: ('SWPP', sorted([int(a),int(b)])),
        'swap letter': lambda a,b: ('SWPL', (a,b)),
        'rotate left': lambda a,b: ('ROTL', int(a)),
        'rotate right': lambda a,b: ('ROTR', int(a)),
        'rotate based': lambda a,b: ('ROTB', b),
        'reverse positions': lambda a,b: ('REVP', (int(a),int(b))),
        'move position': lambda a,b: ('MOVP', (int(a),int(b))),
    }[' '.join(parts[0:2])](parts[2], parts[-1])
    return (op, args)

inp = [parseLine(line.strip()) for line in sys.stdin]

OPS = {
    'SWPP': lambda e, (a, b): e[:a] + e[b:b+1] + e[a+1:b] + e[a:a+1] + e[b+1:],
    'SWPL': lambda e, (a, b): OPS['SWPP'](e, minmax([e.index(a), e.index(b)])),

    'ROTL': lambda e, n: rotate(e, n),
    'ROTR': lambda e, n: rotate(e, -n),
    
    # wtf is this nonsense, AoC?
    'ROTB': lambda e, a: OPS['ROTR'](e, 1 + e.index(a) + (e.index(a) > 3)),
    
    'REVP': lambda e, (a, b): e[:a] + e[a:b+1][::-1] + e[b+1:],
    
    # this one also seems a bit funky..., but is reasonable.
    'MOVP': lambda e, (a, b): wo(e, a)[0:b] + e[a:a+1] + wo(e, a)[b:]
}

def step(s, (op, arg)): return OPS[op](s, arg)

# part 1
print(reduce(step, inp, 'abcdefgh'))

# inverse ops
IOPS = {
    # these should be the same.
    'SWPP': OPS['SWPP'],
    'SWPL': OPS['SWPL'],

    # left becomes right and right becomes left
    'ROTL': OPS['ROTR'],
    'ROTR': OPS['ROTL'],


    # Based on this pattern
    # 0 -> 1
    # 0 + 1 + 0 + 0 ==  1 % 8 == 1
    # 1 -> 3
    # 1 + 1 + 1 + 0 ==  3 % 8 == 7
    # ...
    # 6 -> 6
    # 6 + 1 + 6 + 1 == 14 % 8 == 6
    # 7 -> 0
    # 7 + 1 + 7 + 1 == 16 % 8 == 0
    'ROTB': lambda e, a: IOPS['ROTL'](e, 
        # there's gotta be a cleaner way                          vvvvvvvvvvvvvvvvvvvvv
        ((e.index(a) % 2 == 0) * 3 + e.index(a) / 2) - e.index(a) - 4*(e.index(a) == 0)
    ),
   
    # the inverse of a reverse is the same reverse
    'REVP': OPS['REVP'],
   
    # mov x -> y becomes mov y -> x 
    'MOVP': lambda e, (a, b): OPS['MOVP'](e, (b, a))
}
def istep(s, (op, arg)): return IOPS[op](s, arg)

rinp = inp[::-1]

# checking my work
#rev = reduce(istep, rinp, 'gfdhebac')
#print(rev)
#print('is it correct?', rev == 'abcdefgh')

# part2
print(reduce(istep, rinp, 'fbgdceah'))
