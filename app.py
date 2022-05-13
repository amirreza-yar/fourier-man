from cgi import test
from bin.fourier_series_model import FourierFunc
# from qt_test import CalculatorMain

from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from matplotlib import pyplot as plt

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = CalculatorMain ()
#     win.show()
#     sys.exit(app.exec_())

my_func = FourierFunc (3, -1, 2, 100, "t")
time = np.linspace (-10, 10, 200)

plt.plot (time, my_func.xt (time))
plt.grid ()
plt.show ()