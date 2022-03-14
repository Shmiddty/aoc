OPS = {
    # It might be better to return a static 1 
    # for the offset of hlf, tpl, and inc
    'hlf': lambda r, o: (r / 2, 1),
    'tpl': lambda r, o: (r * 3, 1),
    'inc': lambda r, o: (r + 1, 1),
    'jmp': lambda r, o: (r, o),
    'jie': lambda r, o: (r, o if r % 2 == 0 else 1),
    'jio': lambda r, o: (r, o if r == 1 else 1),
}

def step((op, reg, off), state = None):
    if state == None: state = { 'a': 0, 'b': 0, '_': None }
    if 'a' not in state: state['a'] = 0
    if 'b' not in state: state['b'] = 0
    if '_' not in state: state['_'] = 0

    if reg == None: reg = '_'

    value, offset = OPS[op](state[reg], off) 
    state[reg] = value

    return state, offset 

def run(ops, state = None):
    i = 0
    I = len(ops)

    while i < I:
        op = ops[i]
        state, offset = step(op, state)
        i += offset

    return state

def parseOp(line):
    op = line[0:3]
    parts = line[4:].split(',')
    r = parts[0]
    o = parts[1] if len(parts) > 1 else 1
    if op == 'jmp':
        o = r
        r = None

    return (op, r, int(o))
