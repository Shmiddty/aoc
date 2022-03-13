class Node:
    def __init__(self, value, neighbors = None):
        if neighbors == None: neighbors = set()
        self.value = value
        self.neighbors = neighbors

    def __repr__(self):
        return "Node(%s)"%(str(self.value))
    
    def __str__(self):
        return str(self.value)

    def addNeighbor(self, neighbor):
        self.neighbors.add(neighbor)

class Graph:
    def __init__(self, edges, directed = False):
        self.nodes = dict()
        self.edges = dict()
        self.directed = directed
        
        for edge in edges: self.addEdge(edge)

    def __iter__(self):
        for key in self.nodes:
            yield self.nodes[key]

    def __len__(self):
        return len(self.nodes)
    
    def __getitem__(self, i):
        return self.nodes[i]

    def isConnected(self, a, b):
        return (a,b) in self.edges

    def distance(self, a, b):
        return self.edges[(a,b)]

    def addEdge(self, (a, b, length)):
        H = self.nodes
        A = H[a] if a in H else Node(a)
        B = H[b] if b in H else Node(b)
        
        A.addNeighbor(B)
        self.edges[(A,B)] = length
        if not self.directed:
            self.edges[(B,A)] = length
            B.addNeighbor(A)
        
        H[a] = A
        H[b] = B

    def getNodes(self):
        return self.nodes.values()
