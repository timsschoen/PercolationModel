from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt
from graph_widget import GraphWidget
from graph import Lattice

class PercolationWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout(self)
        self.graphwidget = GraphWidget(self)

        self.graph = Lattice(20,20)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.setPValue)
        self.slider.setValue(100);

        layout.addWidget(self.graphwidget)
        layout.addWidget(self.slider)

        self.setWindowTitle('Percolation Model')

    def updateGraph(self): 
        path = self.graph.findPath(0, 399)      
        self.graphwidget.setPath(self.graph, path)
        self.graphwidget.setGraph(self.graph)

    def setPValue(self, value):
        self.graph.setFractionOfEdges(value/100)
        self.updateGraph()
