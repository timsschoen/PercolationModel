from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QRect
from graph_widget import GraphWidget

class PercolationWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.graphwidget = GraphWidget(self)

        self.graph = None
        self.refresh = False
        self.p = 1

        self.layout.addWidget(self.graphwidget)

        self.infobar = QHBoxLayout()

        self.info_nodes = QLabel(self)
        self.info_nodes.setMinimumHeight(30)
        self.info_nodes.setMaximumHeight(30)
        self.info_edges = QLabel(self)
        self.info_edges.setMinimumHeight(30)
        self.info_edges.setMaximumHeight(30)
        self.info_p = QLabel(self)
        self.info_p.setMinimumHeight(30)
        self.info_p.setMaximumHeight(30)


        self.infobar.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding,QSizePolicy.Minimum))
        self.infobar.addWidget(self.info_p)
        self.infobar.addWidget(self.info_nodes)
        self.infobar.addWidget(self.info_edges)
        self.infobar.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding,QSizePolicy.Minimum))

        self.layout.addLayout(self.infobar)

        self.setMinimumSize(300, 300)

    def setGraph(self,graph):
        self.graph = graph;
        self.updateGraph()

    def setRefresh(self, refresh):
        self.refresh = refresh

    def updateGraph(self): 

        if (self.graph == None):
            return
        self.graph.setFractionOfEdges(self.p, self.refresh)

        #path = self.graph.findPath(0, 399)              
        #self.graphwidget.setPath(self.graph, path)

        self.graphwidget.setGraph(self.graph)

        self.info_nodes.setText("\tNodes: " + str(len(self.graph.nodes)))
        self.info_edges.setText("\tEdges: " + str(len(self.graph.edges)) + ", " + str(self.graph.activeEdgeCount) + " active")

    def setPValue(self, value):
        self.p = value/100
        self.info_p.setText("p = " + str(self.p))
        self.updateGraph()
