import sys

from device import parse, run

iptr, program = parse(sys.stdin.read().strip())
print(run(program, iptr = iptr))

print('---')
# this isn't finishing
print(run(program, [1,0,0,0], iptr = iptr))
