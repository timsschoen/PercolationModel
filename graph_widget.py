
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt

class GraphWidget(QOpenGLWidget):
    
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.layers = []
        self.colorpalette_regions = [
            (1,1,1),
            (1,0.7,0.7),            
            (0.7,1,0.7),
            (0.7,0.7,1)
        ]

        self.colorpalette_paths = [
            (0,0,1),
            (0,1,0),
            (1,0,0),
            (0,1,1),
            (1,0,1),
            (1,1,0)
        ]
        self.dim = 2 
        self.zoom = 1.9
        self.rotation = np.zeros(2)
        self.translation = np.array([-0.5,-0.5,0])

    def paintGL(self):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glRotate(self.rotation[0],1,0,0)
        glRotate(self.rotation[1],0,1,0)
        glScale(self.zoom, self.zoom, self.zoom)
        glTranslate(*self.translation)


        glEnableClientState(GL_VERTEX_ARRAY)
        
        for i in range(len(self.layers)):

            layer = self.layers[i]

            if i == 0:
                glLineWidth(1)
            elif i == 1:
                glLineWidth(3)

            glColor(*layer[1])            
            glVertexPointerf(layer[0])
            glDrawArrays(GL_LINES, 0, len(layer[0]))

        glFlush()

    def setGraph(self, graph, clusters = [], paths = []):
        self.layers = []
        self.dim = graph.dim
        self.rotation = np.zeros(2)
        self.zoom = 1.9
        self.translation = np.array([-0.5,-0.5,0])

        if(self.dim == 3):
            self.rotation[0] = -45
            self.rotation[1] = -45
            self.zoom = 1
            self.translation = np.array([-0.5,-0.5,-0.5])


        if(graph == None):
            return

        layerarray = []

        for e in graph.edges:
            if(e.enabled):
                layerarray.append(list(graph.nodes[e.a]))
                layerarray.append(list(graph.nodes[e.b]))

        self.layers.append((layerarray, (0.6,0.6,0.6)))

        index = 0
        for r in clusters:
            array = []

            for e in graph.edges:
                if(e.enabled and r[e.a] and r[e.b]):
                    array.append(list(graph.nodes[e.a]))
                    array.append(list(graph.nodes[e.b]))

            self.layers.append((array, self.colorpalette_regions[index % len(self.colorpalette_regions)]))
            index += 1

        index = 0
        for p in paths:
            array = []

            for i in range(len(p)-1):                
                array.append(list(graph.nodes[p[i]]))
                array.append(list(graph.nodes[p[i+1]]))

            self.layers.append((array, self.colorpalette_paths[index % len(self.colorpalette_paths)]))
            index += 1

        self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
    
    def initializeGL(self):
        glClearColor(0, 0, 0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Plus):
            self.zoom += 0.1
        elif(event.key() == Qt.Key_Minus):
            self.zoom -= 0.1
        elif(event.key() == Qt.Key_W):
            self.translation[1] -= 0.025
        elif(event.key() == Qt.Key_S):
            self.translation[1] += 0.025
        elif(event.key() == Qt.Key_A):
            self.translation[0] += 0.025
        elif(event.key() == Qt.Key_D):
            self.translation[0] -= 0.025
        elif(event.key() == Qt.Key_Q):
            self.rotation[1] += 5
        elif(event.key() == Qt.Key_E):
            self.rotation[1] -= 5


        self.update()