import sys
import re
from enum import nth, flatten, within
from func import pipe, equals

def parseLine(line):
    names = re.findall(r'[a-z]+', line)
    weight = re.findall(r'\d+', line)
    return names[0], int(weight[0]), names[1:]

inp = [parseLine(line) for line in sys.stdin] 

nodes = map(nth(0), inp)
notBottom = flatten(map(nth(2), inp), 1)

root = filter(pipe(within(notBottom), equals(False)), nodes).pop()
print(root)

# who needs a "fancy" graph class?
def findImbalance(graph, root):
    # I don't like this solution. For one, it doesn't find all imbalances
    # I think, if I were doing this properly, I would construct the graph,
    # map each node to its cumulative weight
    # then traverse the tree-"graph" to find the nodes whose values differ from that of their siblings
    found = []
    def seek(node):
        weight, children = graph[node]
        if len(children) == 0: return (weight, node)

        chs = map(seek, children)
        if len(found): return found[0]
        
        wts = map(nth(0), chs)
        
        if len(set(wts)) > 1:
            offWeight, offNode = filter(lambda (w, n): wts.count(w) == 1, chs).pop()
            onWeight,_ = filter(lambda (w, n): wts.count(w) > 1, chs).pop()
            wt = graph[offNode][0]
            found.append((wt - (offWeight - onWeight), offNode))
            return found[0] 

        return (weight + sum(wts), node)

    return seek(root)

graph = dict(map(lambda (a,b,c): (a,(b,c)), inp))
print(findImbalance(graph, root))
