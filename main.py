import sys
import numpy as np
import math
from PyQt5.QtWidgets import QApplication

from percolation_widget import PercolationWidget

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = PercolationWidget()
   
    w.show()

    sys.exit(app.exec_())

