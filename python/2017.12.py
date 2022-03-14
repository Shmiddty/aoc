import sys
from functools import partial

from graph import Graph
from string import digits
from enum import flatten, decapitate

def distribute((a, ls)): return [(a, b) for b in ls]

def getGroup(node):
    visited = {}
    def seek(n):
        if n in visited: return []
        visited[n] = 1

        return flatten([n] + map(seek, n.neighbors), 1)

    return set(seek(node))

edges = [(a, b, 1) for line in sys.stdin for (a,b) in distribute(decapitate(digits(line)))]
G = Graph(edges, True)
root = G[0]
group = getGroup(root)
print(len(group))

def getGroups(graph):
    nodes = set(graph.getNodes())
    groups = []

    while len(nodes):
        group = getGroup(nodes.pop())
        nodes -= group
        groups.append(group)
    
    return groups

groups = getGroups(G)
print(len(groups))
