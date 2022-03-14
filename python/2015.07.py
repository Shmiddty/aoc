import sys
import re

def safeInt(s):
    return s if s == None or not s.isdigit() else int(s)

def parseLine(line):
    # feels like there should be a more elegant way to do this, but oh well.
    f = re.search(r'([0-9a-z]+)? ?([A-Z]+)? ?([a-z0-9]+)? -> ([a-z]+)', line)
    a = f.group(1)
    OP = f.group(2)
    b = f.group(3)
    c = f.group(4)
    return (c, safeInt(a), OP, safeInt(b))

inp = [parseLine(line.strip()) for line in sys.stdin]

INT16_MAX = (2**16 - 1)
OPS = {
    "AND": lambda A, B: A & B,
    "OR": lambda A, B: A | B,
    "NOT": lambda A, B: INT16_MAX - B,
    "LSHIFT": lambda A, B: INT16_MAX & (A << B),
    "RSHIFT": lambda A, B: INT16_MAX & (A >> B)
}

# Am I just overengineering this?
class Indeterminate:
    def __init__(self):
        self.listeners = []
        self.value = None
        self.key = ""
        self.paused = False

    def __repr__(self):
        return "Intermediate(%s)"%(str(self.value))

    def register(self, cb):
        self.listeners.append(cb)

    def update(self, value):
        self.value = value
        if self.isResolved(): self.broadcast()
        return self

    def broadcast(self):
        if self.paused: return

        for cb in self.listeners:
            cb(self.value)

    def isResolved(self):
        return self.value != None

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

class Variable(Indeterminate):
    @staticmethod
    def normalize(var):
        return var.value if isinstance(var, Variable) else var 

    def __init__(self, value):
        Indeterminate.__init__(self)
        self.value = value
        self.key = None if type(value) == int else value

    def __repr__(self):
        return "Variable(%s)"%(str(self.value))

    def __str__(self):
        return "%s = %s"%(self.key, self.value)

    def isResolved(self):
        return type(self.value) == int

    def resolve(self):
        return self

    def update(self, value):
        val = Variable.normalize(value)
       
        # don't do anything if it hasn't changed
        if self.value == val: return self

        if value == None or type(val) == int: self.value = val
        else: value.register(self.update)

        if self.isResolved(): self.broadcast()
        
        return self
    
    def __rand__(self, other):
        val = Variable.normalize(other)
        if type(self.value) == int and type(val) == int:
            return val & self.value

        return Operator('AND', other, self)

    def __and__(self, other):
        val = Variable.normalize(other)
        if type(self.value) == int and type(val) == int:
            return self.value & val

        return Operator('AND', self, other)

    def __or__(self, other):
        val = Variable.normalize(other)
        if type(self.value) == int and type(val) == int:
            return self.value | val

        return Operator('OR', self, other)

    def __rsub__(self, other):
        if type(self.value) == int:
            return other - self.value

        return Operator('NOT', None, self)

    def __sub__(self, other):
        if type(self.value) == int:
            return self.value - other

        return Operator('NOT', None, other)


    def __rlshift__(self, other):
        val = Variable.normalize(other)
        if type(self.value) == int and type(val) == int:
            return val << self.value

        return Operator('LSHIFT', other, self)

    def __lshift__(self, other):
        val = Variable.normalize(other)
        if type(self.value) == int and type(val) == int:
            return self.value << val

        return Operator('LSHIFT', self, other)

    def __rrshift__(self, other):
        val = Variable.normalize(other)
        if type(self.value) == int and type(val) == int:
            return val >> self.value

        return Operator('RSHIFT', other, self)

    def __rshift__(self, other):
        val = Variable.normalize(other)
        if type(self.value) == int and type(val) == int:
            return self.value >> val

        return Operator('RSHIFT', self, other)

class Operator(Indeterminate):
    def __init__(self, op, left, right):
        Indeterminate.__init__(self)
        self.op = op
        self.left = left
        self.right = right
       
        if isinstance(left, Indeterminate): left.register(self.updateLeft)
        if isinstance(right, Indeterminate): right.register(self.updateRight)

    def __repr__(self):
        return "Operator(%s, %s, %s)"%(self.op, str(self.left), str(self.right))

    def __str__(self):
        return "%s %s %s"%(str(self.left), self.op, str(self.right))

    def isResolved(self):
        L, R = self.left, self.right
        return (L == None or type(L) == int or L.isResolved()) \
           and (R == None or type(R) == int or R.isResolved())

    def updateLeft(self, value):
        self.left = value
        self.resolve()

    def updateRight(self, value):
        self.right = value
        self.resolve()

    def resolve(self):
        L, R = self.left, self.right
        if self.isResolved():
            return self.update(OPS[self.op](self.left, self.right))
       
        return self

    def __rand__(self, other):
        return Operator('AND', other, self)
    def __and__(self, other):
        return Operator('AND', self, other)
    def __or__(self, other):
        return Operator('OR', self, other)
    def __rsub__(self, other):
        return Operator('NOT', None, self)
    def __sub__(self, other):
        return Operator('NOT', None, other)
    def __lshift__(self, other):
        return Operator('LSHIFT', self, other)
    def __rshift__(self, other):
        return Operator('RSHIFT', self, other)


def run(ops, overrides = {}):
    state = {}

    def safeGet(a):
        return state[a] if a in state else Variable(a)

    for (c, a, OP, b) in ops:
        A = safeGet(a)
        B = safeGet(b)
        C = safeGet(c)
        
        if a == A.value and a not in state: state[a] = A
        if b == B.value and b not in state: state[b] = B

        if OP == None and c in overrides: A = Variable(overrides[c])

        state[c] = C.update(A if OP == None else OPS[OP](A, B))

    return state

def part1():
    state = run(inp)
    a = state['a']
    return a.value

print(part1())

def part2():
    state = run(inp, { 'b': part1() })
    a = state['a']
    return a.value

print(part2())
