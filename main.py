import sys
import numpy as np
import math
from lattice import Lattice
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QApplication, QOpenGLWidget

class GridWidget(QOpenGLWidget):
    
    def __init__(self):
        QOpenGLWidget.__init__(self)
        self.vertex_array = []

    def paintGL(self):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glEnableClientState(GL_VERTEX_ARRAY)
                
        glColor(1.0, 0.0, 0.0)

        glVertexPointerf(self.vertex_array)
        glDrawArrays(GL_LINE_STRIP, 0, len(self.vertex_array))
        glFlush()

    def setGrid(self, grid):
        self.vertex_array = []

        for e in grid.edges:
            if(e.enabled):
                self.vertex_array.append(grid.nodes[e.a].array())
                self.vertex_array.append(grid.nodes[e.b].array())

    def resizeGL(self, w, h):
        '''
        Resize the GL window 
        '''
        
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, 1.0, 2, 60.0)
    
    def initializeGL(self):
        '''
        Initialize GL
        '''
        
        # set viewing projection
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, 1.0, 2, 60.0)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    w = GridWidget()
    w.setGrid(Lattice(3,3))
    w.setWindowTitle('Percolation Model')
    w.show()
    
    sys.exit(app.exec_())

