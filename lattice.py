import numpy as np
from grid import Grid
from edge import Edge

class Lattice(Grid):

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

