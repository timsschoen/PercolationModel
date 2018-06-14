import numpy as np
import random
from priority_queue import PriorityQueue

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.enabled = True

class Graph:
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.activeEdgeCount = 0
        self.dim = 2

    def findPath(self, startID, endID):
        Queue = PriorityQueue()

        G = self.asAdjacencyList()

        visited = set()

        parent = {}
        cost_array = np.zeros(len(self.nodes))

        Queue.add_update(startID, 0)

        found = False

        while (not Queue.empty()):

            node = Queue.pop()

            if(node == endID):
                found = True
                break

            visited.add(node)

            for nextNode in G[node]:

                if(nextNode in visited):
                    continue

                newcost = cost_array[node] + np.linalg.norm(self.nodes[node]-self.nodes[nextNode])

                if(nextNode in Queue and newcost >= cost_array[nextNode]):
                    continue

                parent[nextNode] = node
                cost_array[nextNode] = newcost

                f = newcost + np.linalg.norm(self.nodes[endID]-self.nodes[nextNode])

                Queue.add_update(nextNode, f);

        if(not found):
            return []
            
        path = []

        node = endID
        while(node != startID):
            path.append(node)
            node = parent[node]

        path.append(node)

        path.reverse()

        return path


    def asAdjacencyList(self):
        A = {};

        for n in range(len(self.nodes)):
            A[n] = set()

        for e in self.edges:
            if(e.enabled):
                A[e.a].add(e.b)
                A[e.b].add(e.a)

        return A

    def setFractionOfEdges(self, fraction):
        size = len(self.edges)
        target = fraction*size
        change = target-self.activeEdgeCount

        while (change > 0):
            while(True):
                index = np.random.randint(0, size)
                if( self.edges[index].enabled == False):
                    self.edges[index].enabled = True
                    self.activeEdgeCount += 1
                    change -= 1
                    break

        while (change < 0):
            while(True):
                index = np.random.randint(0, size)
                if( self.edges[index].enabled):
                    self.edges[index].enabled = False
                    self.activeEdgeCount -= 1
                    change += 1
                    break

    def __str__(self):

        result = "Nodes:\n"
        for i in range(len(self.nodes)):
            result += str(i) + ": " + str(self.nodes[i]) + "\n"

        result += "Edges:\n"
        for e in self.edges:
            result += "From " + str(e.a) + " to " + str(e.b) + (" - enabled" if e.enabled else " - disabled") + "\n"

        result += "Total vertex count: " + str(len(self.nodes)) + "\n"
        result += "Total edge count: " + str(len(self.edges)) + "\n"
        result += "Active edge count: " + str(self.activeEdgeCount)

        return result;


class Lattice(Graph):

    def __init__(self,width, height):
        super(Lattice, self).__init__()
        xsteps = 1/(width-1)
        ysteps = 1/(height-1)

        self.dim = 2

        for x in range(width):
            for y in range(height):
                self.nodes.append(np.array([x*xsteps, y*ysteps]))

                if(y != height-1):                    
                    self.edges.append(Edge(x*height+y, x*height+(y+1)))
                    self.activeEdgeCount = self.activeEdgeCount + 1
                if(x != width-1):
                    self.edges.append(Edge(x*height+y, (x+1)*height+y))
                    self.activeEdgeCount = self.activeEdgeCount + 1