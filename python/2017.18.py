import sys

# this is so inelegant, isn't it? Guess I'm a terrible person and don't deserve to exist.
class compy:
    def __init__(self, state = None):
        if state == None: state = {} 
        self.reg = state
        self.last = None
    
    def __getitem__(self, i):
        return (self.reg[i] if i in self.reg else 0) if i.islower() else int(i)

    def __setitem__(self, i, val):
        self.reg[i] = val

    def reset(self):
        self.reg = {}
        self.last = None

    def snd(self, r, y):
        self.last = self[r]
        return 1

    def set(self, r, y):
        self[r] = self[y]
        return 1

    def add(self, r, y):
        self[r] += self[y]
        return 1

    def mul(self, r, y):
        self[r] *= self[y]
        return 1

    def mod(self, r, y):
        self[r] %= self[y]
        return 1

    def rcv(self, r, y):
        if self[r]:
            raise Exception(self.last)
        return 1

    def jgz(self, r, y):
        return self[y] if self[r] > 0 else 1
    
    def run(self, program):
        cur = 0
        L = len(program)
        while cur < L:
            op, r, y = program[cur]
            cur += getattr(self, op)(r, y)

def parseLine(line):
    parts = line.strip().split(' ')
    if len(parts) < 3: parts += ['0']
    return parts

inp = [parseLine(line) for line in sys.stdin]

mindi = compy()
try: mindi.run(inp)
except: print(sys.exc_info()[1]) 

class compy2(compy):
    def snd(self, r, y):
        self.outgoing.append(self[r])
        return 1

    def rcv(self, r, y):
        self[r] = self.incoming.pop(0)
        return 1

# it's kinda awkward to do this synchronously, 
def runner(prog, a, b):
    # run a until rcv, then swap to b, etc
    C = [0, 0]      # cursors
    P = [a, b]      # programs
    q = [[], []]    # queues
    s = [0, 0]      # count of sends
    p = 0           # current program
    R = 0           # number of unmet receives

    L = len(prog)

    a.incoming = q[0]
    a.outgoing = q[1]
    b.incoming = q[1]
    b.outgoing = q[0]
    
    while 1:
        comp = P[p]
        c = C[p]
        op, r, y = prog[c]
        
        if op == 'rcv' and not len(comp.incoming):
            # nothing to receive, swap to other program
            p = (p + 1) % len(P)
            
            R += 1              # count of unmet receives
            if R == 2: break    # deadlocked
            
            continue

        if op == 'snd':
            R = 0               # reset count of unmet receives
            s[p] += 1
        
        c += getattr(comp, op)(r, y)
        C[p] = c # update the cursor for the current program

    return s[1] # return the number of times that program 1 sent a value

print(runner(inp, compy2({ 'p': 0 }), compy2({ 'p': 1 })))
# 11938 is too high
# 6096 is still too high because that was for program 0, you dummy.
