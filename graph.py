import numpy as np
import random
from priority_queue import PriorityQueue
from queue import Queue

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.enabled = True

class Graph:
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.active_edge_count = 0

    def findClusters(self):
        clusters = np.zeros(len(self.nodes))

        G = self.asAdjacencyList()

        cluster_count = 0
        largest_cluster = 0
        largest_cluster_size = 0

        for i in range(len(self.nodes)):

            if(clusters[i] != 0):
                continue

            cluster_count += 1

            clusters[i] = cluster_count

            queue = Queue()

            queue.put(i)

            cluster_size = 0

            while (not queue.empty()):
                index = queue.get()

                for neighbour in G[index]:

                    if(clusters[neighbour] != 0):
                        continue

                    clusters[neighbour] = cluster_count
                    queue.put(neighbour)
                    cluster_size += 1

            if(cluster_size > largest_cluster_size):
                largest_cluster_size = cluster_size
                largest_cluster = cluster_count
        
        return (clusters, largest_cluster, largest_cluster_size)   

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

    def setFractionOfEdges(self, fraction, refresh):        

        if(refresh):
            draw = np.random.binomial(1, fraction, len(self.edges))
            self.active_edge_count = draw.sum()
            for i in range(len(self.edges)):
                self.edges[i].enabled = (draw[i] == 1)
        else:
            size = len(self.edges)
            target = fraction*size
            change = target-self.active_edge_count

            while (change > 0):
                while(True):
                    index = np.random.randint(0, size)
                    if( self.edges[index].enabled == False):
                        self.edges[index].enabled = True
                        self.active_edge_count += 1
                        change -= 1
                        break

            while (change < 0):
                while(True):
                    index = np.random.randint(0, size)
                    if( self.edges[index].enabled):
                        self.edges[index].enabled = False
                        self.active_edge_count -= 1
                        change += 1
                        break
    
    def getTopBoundary(self):
        pass

    def getBottomBoundary(self):
        pass

    def __str__(self):

        result = "Nodes:\n"
        for i in range(len(self.nodes)):
            result += str(i) + ": " + str(self.nodes[i]) + "\n"

        result += "Edges:\n"
        for e in self.edges:
            result += "From " + str(e.a) + " to " + str(e.b) + (" - enabled" if e.enabled else " - disabled") + "\n"

        result += "Total vertex count: " + str(len(self.nodes)) + "\n"
        result += "Total edge count: " + str(len(self.edges)) + "\n"
        result += "Active edge count: " + str(self.active_edge_count)

        return result


class Lattice_2d(Graph):

    dim = 2

    def __init__(self,size):
        super(Lattice_2d, self).__init__()
        xsteps = 1/(size-1)
        ysteps = 1/(size-1)
        self.size = size

        for x in range(size):
            for y in range(size):
                self.nodes.append(np.array([x*xsteps, y*ysteps]))

                if(y != size-1):                    
                    self.edges.append(Edge(x*size+y, x*size+(y+1)))
                if(x != size-1):
                    self.edges.append(Edge(x*size+y, (x+1)*size+y))

        self.active_edge_count = len(self.edges)

    def getBottomBoundary(self):
        result = np.zeros(self.size*self.size).astype(bool)
        for x in range(self.size):
            result[x*self.size + self.size-1] = True
        return result

    def getTopBoundary(self):
        result = np.zeros(self.size*self.size).astype(bool)
        for x in range(self.size):
            result[x*self.size] = True
        return result

class Lattice_3d(Graph):

    dim = 3

    def __init__(self,size):
        super(Lattice_3d, self).__init__()
        stepsize = 1/(size-1)


        for x in range(size):
            for y in range(size):
                for z in range(size):
                    self.nodes.append(np.array([x*stepsize, y*stepsize, z*stepsize]))

                    if(y != size-1):                    
                        self.edges.append(Edge(x*size*size+y*size+z, x*size*size + (y+1)*size + z))
                    if(x != size-1):
                        self.edges.append(Edge(x*size*size+y*size+z, (x+1)*size*size + y*size + z))
                    if(z != size-1):
                        self.edges.append(Edge(x*size*size+y*size+z, x*size*size + y*size + (z+1)))

        self.active_edge_count = len(self.edges)

class Triangles_2d(Graph):

    dim = 2

    def __init__(self,size):
        super(Triangles_2d, self).__init__()
        xsteps = 1/(size-1)
        ysteps = 1/(size-1)
        self.size = size

        for x in range(size):
            for y in range(size):
                self.nodes.append(np.array([x*xsteps, y*ysteps]))

                if(y != size-1):                    
                    self.edges.append(Edge(x*size+y, x*size+(y+1)))
                if(x != size-1):
                    self.edges.append(Edge(x*size+y, (x+1)*size+y))
                if(x != size-1 and y != size-1):                    
                    self.edges.append(Edge(x*size+y, (x+1)*size+(y+1)))

        self.active_edge_count = len(self.edges)

    def getBottomBoundary(self):
        result = np.zeros(self.size*self.size).astype(bool)
        for x in range(self.size):
            result[x*self.size + self.size-1] = True
        return result

    def getTopBoundary(self):
        result = np.zeros(self.size*self.size).astype(bool)
        for x in range(self.size):
            result[x*self.size] = True
        return result

class Honeycomb_2d(Graph):

    dim = 2

    def __init__(self,size):
        super(Honeycomb_2d, self).__init__()

        size -= size % 3
        self.size = size

        stepsize = 1/(size-1)

        rowlength = 2*int(size / 3)

        for y in range(size):

            nodes_in_row = 0

            for x in range(size):

                if y % 2 == 0 and x % 3 == 2:
                    continue

                if y % 2 == 1 and x % 3 == 1:
                    continue

                self.nodes.append(np.array([x*stepsize - (y % 2)*(stepsize/2), y*stepsize]))

                index = y*rowlength + nodes_in_row

                if(y % 2 == 0 and x % 3 == 0):       
                    if( y != size-1):           
                        self.edges.append(Edge(index, index + rowlength))
                    if (x != size-1):                        
                        self.edges.append(Edge(index, index+1))

                if(y % 2 == 0 and x % 3 == 1):       
                    if y != size-1:           
                        self.edges.append(Edge(index, index + rowlength))

                if(y % 2 == 1 and x % 3 == 0):       
                    if( y != size-1):           
                        self.edges.append(Edge(index, index + rowlength))

                if(y % 2 == 1 and x % 3 == 2):       
                    if( y != size-1):           
                        self.edges.append(Edge(index, index + rowlength))
                    if (x != size-1):                        
                        self.edges.append(Edge(index, index+1))

                nodes_in_row += 1

        self.active_edge_count = len(self.edges)

    def getBottomBoundary(self):
        result = np.zeros(len(self.nodes)).astype(bool)
        rowlength = 2*int(self.size / 3)

        for y in range(self.size):

            nodes_in_row = 0

            for x in range(self.size):

                if y % 2 == 0 and x % 3 == 2:
                    continue

                if y % 2 == 1 and x % 3 == 1:
                    continue

                index = y*rowlength + nodes_in_row

                if(y == 0):
                    result[index] = 1
        return result

    def getTopBoundary(self):
        result = np.zeros(len(self.nodes)).astype(bool)
        rowlength = 2*int(self.size / 3)

        for y in range(self.size):

            nodes_in_row = 0

            for x in range(self.size):

                if y % 2 == 0 and x % 3 == 2:
                    continue

                if y % 2 == 1 and x % 3 == 1:
                    continue

                index = y*rowlength + nodes_in_row

                if(y == self.size-1):
                    result[index] = 1
        return result