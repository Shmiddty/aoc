import sys
import re
from itertools import permutations
from graph import Graph

def parseLine(line):
    parts = re.search(r'(\w+) to (\w+) = (\d+)', line)
    result = (parts.group(1), parts.group(2), int(parts.group(3)))
    return result

inp = [parseLine(line.strip()) for line in sys.stdin]

def getPathLength(graph):
    return lambda path: sum(map(lambda (a,b): graph.distance(a,b), zip(path, path[1:])))

def getAllRoutes(graph):
    # all permutations of all nodes
    # this might be less efficient than traversing the graph, but it sure is easy.
    paths = list(permutations(graph))
    #l1 = len(paths)
    # remove disjointed paths.
    # turns out this wasn't necessary (at least for my input)
    #paths = filter(
    #    lambda path: all(map(
    #        lambda (a,b): graph.isConnected(a, b), 
    #        zip(path, path[1:])
    #    )),
    #    paths
    #)
    #l2 = len(paths)
    #print(l1, l2)
    return paths

graph = Graph(inp)
measure = getPathLength(graph)
routes = getAllRoutes(graph)

# I'm not sure that I actually need a graph for this
# since there are no duplicate edges in the input
def part1():
    return min(map(measure, routes))

print(part1())

def part2():
    return max(map(measure, routes))

print(part2())
