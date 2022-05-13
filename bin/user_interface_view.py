import functools
import sys
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QGroupBox, QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

from bin.fourier_series_model import FourierFunc

# CREATIGN THE MATPLOTLIB API TO WORK WITH PYPLOT
class PltCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100) -> None:
        # fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(PltCanvas, self).__init__(self.fig)

# THE MAIN UI
class UserInterface(QMainWindow):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        # SETTING THE BASE CONFIGS FOR GUI
        self.setWindowTitle("Fourier Man")
        self._centralwidget = QWidget(self)
        self.setCentralWidget(self._centralwidget)
        self._centrallayout = QVBoxLayout()
        self._centralwidget.setLayout (self._centrallayout)
        
        self.xt_graph = PltCanvas()
        self.xt_fig = self.xt_graph.fig
        
        self._add_input_sec()

        self.temp_num = 0

        # self.xt_data = self._find_series()
        # self.line1, = self.xt_graph.ax1.plot(0, self.xt_data, 'ro')
        # # self.xt_data += 0.02
        # # self.line1.set_ydata(self.xt_data + 0.02)
        # # self.line1.set_ydata(myfunction.xt(time))
        # self.graph_groupbox_layout.addWidget(self.xt_graph)

        # self._add_graph_sec()

    def _find_series(self, time = 0):
        input_func_text = self.input_func.text()
        myfunction = FourierFunc(3, -1, 2, 5, input_func_text)
        return myfunction.xt(time)

    def _draw_button(self):
        self.xt_fig.canvas.flush_events ()
        self.temp_num += 0.01
        time = np.linspace(-5, 5, 500)
        new_series = self._find_series(time)
        # print(np.min(new_series), np.max(new_series))
        self.ax1.set_ylim ([np.min(new_series) - 0.2, np.max(new_series) + 0.2])
        self.line1.set_ydata(new_series)
        self.xt_fig.canvas.draw()
        # sleep (0.01)

    def _plot_graph(self, input_func = "2*t + 1"):
        time = np.linspace(-5, 5, 500)
        self.ax1 = self.xt_fig.add_subplot(111)
        xt_data = self._find_series(time)
        self.line1, = self.ax1.plot(time, xt_data, 'r-')
        self.graph_groupbox_layout.addWidget(self.xt_graph)


    def _add_input_sec(self):
        graph_groupbox = QGroupBox("Graphs")
        graph_groupbox.setCheckable(True)
        self.graph_groupbox_layout = QVBoxLayout()
        graph_groupbox.setLayout(self.graph_groupbox_layout)
        self._centrallayout.addWidget(graph_groupbox)

        self.input_func = QLineEdit()
        self.graph_groupbox_layout.addWidget(self.input_func)
        self.input_func.setText("2*t + 1")

        self._plot_graph()

        draw_button = QPushButton("Draw")
        draw_button.clicked.connect(self._draw_button)
        self.graph_groupbox_layout.addWidget(draw_button)
        # self.xt_r_graph = PltCanvas()
        # self.xt_r_graph.axes.plot([1, 2, 3, 4,], [4, 2, 1, 3,])
        # self.graph_groupbox_layout.addWidget(self.xt_r_graph)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = UserInterface()
    win.show()
    sys.exit(app.exec_())