
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QApplication, QOpenGLWidget

class GraphWidget(QOpenGLWidget):
    
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.vertex_array = []
        self.path_vertex_array = []

    def paintGL(self):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glEnableClientState(GL_VERTEX_ARRAY)
                
        glColor(1.0, 0.0, 0.0)

        glVertexPointerf(self.vertex_array)
        glDrawArrays(GL_LINES, 0, len(self.vertex_array))

        glColor(0.0, 0.0, 1.0)

        glVertexPointerf(self.path_vertex_array)
        glDrawArrays(GL_LINES, 0, len(self.path_vertex_array))

        glFlush()

    def setGraph(self, graph):
        self.vertex_array = []

        for e in graph.edges:
            if(e.enabled):
                self.vertex_array.append(list(graph.nodes[e.a]-np.array([0.5,0.5])))
                self.vertex_array.append(list(graph.nodes[e.b]-np.array([0.5,0.5])))

        self.update()

    def setPath(self, graph, path):
        self.path_vertex_array = []

        for i in range(len(path)-1):
            self.path_vertex_array.append(list(graph.nodes[path[i]]-np.array([0.5,0.5])))
            self.path_vertex_array.append(list(graph.nodes[path[i+1]]-np.array([0.5,0.5])))

        self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
    
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()