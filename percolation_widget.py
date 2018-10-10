from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from graph_widget import GraphWidget
import numpy as np

class PercolationWidget(QWidget):

    graphUpdated = pyqtSignal(float, float)

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
        self.info_clustersize = QLabel(self)
        self.info_clustersize.setMinimumHeight(30)
        self.info_clustersize.setMaximumHeight(30)

        self.infobar.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding,QSizePolicy.Minimum))
        self.infobar.addWidget(self.info_p)
        self.infobar.addWidget(self.info_nodes)
        self.infobar.addWidget(self.info_edges)
        self.infobar.addWidget(self.info_clustersize)
        self.infobar.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding,QSizePolicy.Minimum))

        self.layout.addLayout(self.infobar)

        info = QLabel(self)
        info.setMinimumHeight(30)
        info.setMaximumHeight(30)
        info.setText("Press +/- to zoom, WASD for panning or Q/E for rotating.")

        infolayout = QHBoxLayout()
        infolayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding,QSizePolicy.Minimum))
        infolayout.addWidget(info)
        infolayout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding,QSizePolicy.Minimum))

        self.layout.addLayout(infolayout)

        self.setMinimumSize(300, 300)

    def setGraph(self,graph):
        self.graph = graph
        self.updateGraph()

    def setRefresh(self, refresh):
        self.refresh = refresh

    def updateGraph(self): 

        if (self.graph == None):
            return
        self.graph.setFractionOfEdges(self.p, self.refresh)

        clusters, largest_cluster, largest_cluster_size = self.graph.findClusters()

        region = (clusters == largest_cluster)

        # get the masks indicating which node belongs to top- or bottomboundary
        # as defined by the grid type
        bottomboundary = self.graph.getBottomBoundary()
        topboundary = self.graph.getTopBoundary()

        bottomrow = clusters[bottomboundary]
        toprow = clusters[topboundary]

        # find the indices in top- and bottomrow belonging belonging to the same cluster
        same, b, c = np.intersect1d(toprow,bottomrow, return_indices=True)

        if(len(b) > 0):
            # use np.nonzero to get the indices from the masks
            print(np.nonzero(bottomboundary))
            bottomindex_graph = np.nonzero(bottomboundary)[0][c][0]
            topindex_graph = np.nonzero(topboundary)[0][b][0]
            print("path from " + str(bottomindex_graph) + " to " + str(topindex_graph))
            path = self.graph.findPath(bottomindex_graph, topindex_graph)
            self.graphwidget.setGraph(self.graph, [region], [path])
        else:
            self.graphwidget.setGraph(self.graph, [region], [])

        self.info_nodes.setText("\tNodes: " + str(len(self.graph.nodes)))
        self.info_edges.setText("\tEdges: " + str(len(self.graph.edges)) + ", " + str(self.graph.active_edge_count) + " active")
        self.info_clustersize.setText("\tLargest cluster: " + "{:.2f}".format(100*largest_cluster_size/len(self.graph.nodes)) + " %")
        self.graphUpdated.emit(self.p, largest_cluster_size/len(self.graph.nodes))

    def setPValue(self, value):
        self.p = value/100
        self.info_p.setText("p = " + str(self.p))
        self.updateGraph()


