import numpy as np
import random
from edge import Edge

class Grid:
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.activeEdgeCount = 0
        self.dim = 2

    def findPath(self):
        pass

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
        for i in range(len(self.nodes))
            result += str(i) + ": " + str(self.nodes[i]) + "\n"

        result += "Edges:\n"
        for e in self.edges:
            result += "From " + str(e.a) + " to " + str(e.b) + (" - enabled" if e.enabled else " - disabled") + "\n"

        result += "Total vertex count: " + str(len(self.nodes)) + "\n"
        result += "Total edge count: " + str(len(self.edges)) + "\n"
        result += "Active edge count: " + str(self.activeEdgeCount)

        return result;

