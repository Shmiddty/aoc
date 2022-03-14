import sys

from enum import chunk, flatten
from func import repeat, iterN, pipe, callwith, curry, equals

# mebbe new tool?
def spread(fn): return lambda ls: fn(*ls)

# this is the slow way
def chunk2d(mat, rx = 2, ry = None):
    if ry == None: ry = rx
    return map(
        lambda a: zip(*map(lambda b: chunk(b, rx), a)), # this one would be obnoxious
        chunk(mat, ry)
    )

# It feels like the explosion and restitching process could be done more efficiently
def restitch(expl):
    return flatten(map(
        curry(map, pipe(
            list,       # since we can't flatten tuples
            flatten,    # combine the nested chunks
            #curry(map, str), # don't need this here
            ''.join     # then the row list into a string
        )), 
        map(spread(zip), expl)
    )) 

def parseLine(line):
    a, b = line.strip().split(' => ')
    return a.split('/'), b.split('/') 

def flipY(pat): return pat[::-1]
def flipX(pat): return map(flipY, pat) # sneaky sneaky
def rotate(pat): return map(''.join, zip(*flipY(pat))) # zipYflipY

def variations(pat):
    rots = iterN(rotate, 4)(list(pat))
    return set(map('/'.join, rots + map(flipX, rots) + map(flipY, rots)))

rules = {
    key:b
    for a, b in [parseLine(line) for line in sys.stdin]
    for key in variations(a) # creating the variations up front saves a lot of time
}
init = ['.#.','..#','###']

def enhancer(rules):
    def enhance(pattern):
        return rules['/'.join(pattern)]
        # this was slowing me down
        #for pat in variations(pattern):
        #    if pat in rules:
        #        return rules[pat]

    return enhance

def stepper(enhance = enhancer(rules)):
    def step(mat):
        foo = restitch(map(curry(map, enhance), chunk2d(mat, 2 + len(mat) % 2)))
        return foo

    return step

def count(pattern):
    return sum(map(pipe(curry(map, equals('#')), sum), pattern))

five = repeat(stepper(), init)(5)
print(count(five))

# odds on this not finishing?
# pretty low. it finished in about 7 seconds
# very very slow
# the time difference is not even discernable between starting 
# from the initial value and the value after five steps
# after pre-generating the variations, it's down to about 1 second
# if I optimize the explosion/stitching, I think it could be faster
eighteen = repeat(stepper(), five)(13)
print(count(eighteen))
