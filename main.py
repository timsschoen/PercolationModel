import sys
import numpy as np
import math
from PyQt5.QtWidgets import QApplication


from app_widget import AppWidget


if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = AppWidget()
   
    w.resize(1500,750)
    w.show()

    sys.exit(app.exec_())

