import sys
import re
from functools import partial
sys.path.insert(0, './lib/')
from func import equals
from maths import product

# Not particularly fond of this method of input parsing. 
def parseLine(line):
    if line[0] == 'v':
        val, bot = re.findall(r'\d+', line)
        return (int(val), 'bot ' + bot)
    else: 
        parts = re.search(r'(bot \d+) gives low to ([^\d]+ \d+) and high to ([^\d]+ \d+)', line)
        source = parts.group(1)
        lowDest = parts.group(2)
        highDest = parts.group(3)
        return (source, lowDest, highDest)

inp = [parseLine(line) for line in sys.stdin]

def receive(state, key, val):
    state[key] = val
    return state

# icky hardcoded global can't be bothered values
check = [61, 17]
def give(state, key, *args):
    if len(args) < 4:
        state[key] = partial(give, state, key, *args)
        return state[key]

    dLow, dHigh, v1, v2 = args

    # this is super icky
    if v1 in check and v2 in check:
        print(key) # part 1

    get(state, dLow)(min(v1, v2))
    get(state, dHigh)(max(v1, v2))

def get(state, key):
    if key not in state:
        state[key] = give(state, key) if "bot" in key else partial(receive, state, key)

    return state[key]

def step(state, op):
    if len(op) == 3:
        b, ld, hd = op
        get(state, ld)
        get(state, hd)
        get(state, b)(ld, hd)
    else:
        v, b = op
        get(state, b)(v)

    return state

# It's better to give the gifts at the end of the party. 
sort = sorted(inp, key=len, reverse=True)
state = reduce(step, sort, {})
outputs = { key: state[key] for key in state if 'output' in key }
part2 = map(lambda v: 'output ' + str(v), range(3))
print(product(map(outputs.get, part2)))
