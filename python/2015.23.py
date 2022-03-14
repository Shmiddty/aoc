import sys
import computer as C

inp = [C.parseOp(line.strip()) for line in sys.stdin]

print(C.run(inp)['b'])
print(C.run(inp, { 'a': 1 })['b'])
