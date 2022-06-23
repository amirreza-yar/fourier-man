# from cgi import test
from src.fourier_series_model import FourierSeries
from src.gui_view import FourierManGui
# from qt_test import CalculatorMain

from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FourierManGui()
    win.show()
    sys.exit(app.exec_())