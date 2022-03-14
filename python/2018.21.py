import sys

from device import parse, run

iptr, program = parse(sys.stdin.read().strip())

class reghax(list):
    def __getitem__(self, key):
        if key == 0:
            # eqrr 2 0 3
            # is the only instruction that accesses register 0 for my input
            # it compares it to the value in register 2
            # so if we just return the value in register 2...
            # it should be the correct answer, right?
            val = list.__getitem__(self, 2)
            # part 1
            print(val) # 13970209
            return val

        return list.__getitem__(self, key)

run(program, reg = reghax([0,0,0,0]), iptr = iptr)

class reghax2(list):
    def __getitem__(self, key):
        if key == 0:
            # eqrr 2 0 3
            # is the only instruction that accesses register 0 for my input
            # it compares it to the value in register 2
            # so if we just return the value in register 2...
            # it should be the correct answer, right?
            val = list.__getitem__(self, 2)
            # part 1
            print(val) # 13970209
            #return val

        return list.__getitem__(self, key)

run(program, reg = reghax2([0,0,0,0]), iptr = iptr)

