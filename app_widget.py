from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from graph_widget import GraphWidget
from graph import Lattice_2d, Triangles_2d
from percolation_widget import PercolationWidget
from pyqtgraph import PlotWidget

class AppWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.graph_types = [Lattice_2d,Triangles_2d]
        self.graph_names = ["2d-Lattice", "2d-Triangles"]

        self.setupLayout()
        self.setSettings()

    def setSettings(self):        
        self.graph_type_combobox.setCurrentIndex(0)
        self.p_slider.setValue(100) 
        self.N_slider.setValue(30)
        self.refresh_edges_checkbox.setCheckState(Qt.Checked)    

    def setupLayout(self):
        self.layout = QHBoxLayout(self)
        self.splitter = QSplitter(Qt.Horizontal)

        self.settingswidget = QWidget(self)
        self.settingswidget.setMaximumWidth(400)
        self.settingslayout = QVBoxLayout()

        self.percolationWidget = PercolationWidget()

        self.graph_type_combobox = QComboBox(self)
        self.graph_type_combobox.addItems(self.graph_names)
        self.graph_type_combobox.currentIndexChanged.connect(self.handleGraphTypeChanged)
        self.settingslayout.addWidget(self.graph_type_combobox)

        self.p_slider_layout = QHBoxLayout()
        self.settingslayout.addLayout(self.p_slider_layout)

        self.p_slider_layout.addWidget(QLabel("Set p value: ", self))

        self.p_slider_label = QLabel(self)

        self.p_slider = QSlider(Qt.Horizontal, self)
        self.p_slider.valueChanged.connect(self.handlePSliderChange)

        self.p_slider_layout.addWidget(self.p_slider)
        self.p_slider_layout.addWidget(self.p_slider_label)

        self.N_slider_layout = QHBoxLayout()
        self.settingslayout.addLayout(self.N_slider_layout)

        self.N_slider_layout.addWidget(QLabel("Set size (N): ", self))

        self.N_slider_label = QLabel(self)

        self.N_slider = QSlider(Qt.Horizontal, self)
        self.N_slider.valueChanged.connect(self.handleNSliderChange)

        self.N_slider_layout.addWidget(self.N_slider)
        self.N_slider_layout.addWidget(self.N_slider_label)

        # wether to refresh edges each time or keep edges to add to/remove from
        self.refresh_edges_checkbox = QCheckBox("Refresh Edges instead of Adding/Removing", self)
        self.refresh_edges_checkbox.stateChanged.connect(self.handleRefreshCheckboxChange)

        self.plot_widget = PlotWidget()

        self.settingslayout.addWidget(self.refresh_edges_checkbox)

        self.settingslayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.settingswidget.setLayout(self.settingslayout)
        self.settingswidget.setMinimumSize(50, 50)

        self.splitter.addWidget(self.settingswidget)
        self.splitter.addWidget(self.percolationWidget)

        self.layout.addWidget(self.splitter)

        self.setWindowTitle('Percolation Model')

    def handleGraphTypeChanged(self,index):
        self.graph = self.graph_types[index](self.N_slider.value())
        self.percolationWidget.setGraph(self.graph)

    def handlePSliderChange(self, value):
        self.percolationWidget.setPValue(value)
        self.p_slider_label.setText(str(value) + " %")

    def handleNSliderChange(self, value):
        self.graph = self.graph_types[self.graph_type_combobox.currentIndex()](value)
        self.percolationWidget.setGraph(self.graph)
        self.N_slider_label.setText(str(value))

    def handleRefreshCheckboxChange(self, value):
        self.percolationWidget.setRefresh(value == Qt.Checked)


