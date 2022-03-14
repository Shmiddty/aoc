import sys
import re
from itertools import permutations
from graph import Graph

def parseLine(line):
    parts = re.search(r'(\S+) would (\S+) (\d+) .* (\w+)\.$', line)
    a = parts.group(1)
    b = parts.group(4)
    s = (parts.group(2) == "gain") * 2 - 1
    d = int(parts.group(3))
    return (a, b, s * d)

inp = [parseLine(line.strip()) for line in sys.stdin]

def getHappiness(graph):
    return lambda seats: sum(map(
        lambda (a, b): graph.distance(a, b) + graph.distance(b, a), 
        zip(seats, seats[1:] + seats[0:1]) # make it a circle!
    ))

def part1():
    graph = Graph(inp, True)
    measure = getHappiness(graph)
    seatings = permutations(graph)
    scored = map(measure, seatings)
    
    return max(scored)

print(part1())

def part2():
    graph = Graph(inp, True)
   
    # Let me just squeeeeeeze in here. 
    for guest in graph.getNodes():
        graph.addEdge(('me', guest.value, 0))
        graph.addEdge((guest.value, 'me', 0))

    measure = getHappiness(graph)
    # much slower with an additional node
    seatings = permutations(graph)
    scored = map(measure, seatings)
    
    return max(scored)

print(part2())
