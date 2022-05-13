# IMPORTING THE NEEDED MODULES FROM PYAT5 AND NUMPY
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QGroupBox, QLineEdit, QTableWidget,
    QHeaderView, QSizePolicy, QAbstractScrollArea
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import sys

# IMPORTING THE LOCAL MODULES
from fourier_series_model import FourierSeries

# CREATIGN THE MATPLOTLIB API CLASS TO WORK ON PYPLOT SYS
class PltCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100) -> None:
        # SETTING THE FIGURE INSTANCE
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(PltCanvas, self).__init__(self.fig)

class FourierManGui(QMainWindow):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        # SETTING THE BASE CONFIGS FOR MAIN WINDOW
        self.setWindowTitle("Fourier Man")
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralLayout = QHBoxLayout()
        self._centralWidget.setLayout (self._centralLayout)

        # INJECTING A PYPLOT INSTANCE TO THE GUI
        self.xt_graph = PltCanvas()
        # self.xt_fig = self.xt_graph.fig

        self._createInputTable()
        # self._add_input_sec()

    def _createInputTable(self):
        self.inputTable = QTableWidget(3, 2)
        self.inputTable.setHorizontalHeaderLabels(["Function", "Boundary"])
        tableHorHeader = self.inputTable.horizontalHeader()
        tableHorHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        tableHorHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        # self.inputTable.setGeometry(0, 0, 0, 0)
        # self.inputTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.inputTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.inputTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self._centralLayout.addWidget(self.inputTable)
        # tableVerHeader = self.inputTable.verticalHeader()
        # tableVerHeader.setSectionResizeMode(0, QHeaderView.Fixed)

    def _findSeries(self, time = 0):
        myfunction = FourierSeries(3, -1, 2, 5, "2*t + 1")
        return myfunction.xt(time)

    # def _draw_button(self):
    #     self.xt_fig.canvas.flush_events ()
    #     time = np.linspace(-5, 5, 500)
    #     new_series = self._find_series(time)
    #     # print(np.min(new_series), np.max(new_series))
    #     self.ax1.set_ylim ([np.min(new_series) - 0.2, np.max(new_series) + 0.2])
    #     self.line1.set_ydata(new_series)
    #     self.xt_fig.canvas.draw()
        # sleep (0.01)

    def _plotGraph(self):
        time = np.linspace(-5, 5, 500)
        xtFig = self.xt_graph.fig
        ax1 = xtFig.add_subplot(111)
        xt_data = self._findSeries(time)
        self.line1, = ax1.plot(time, xt_data, 'r-')
        self._centralLayout.addWidget(self.xt_graph)


    # def _add_input_sec(self):
    #     graph_groupbox = QGroupBox("Graphs")
    #     graph_groupbox.setCheckable(True)
    #     self.graph_groupbox_layout = QVBoxLayout()
    #     graph_groupbox.setLayout(self.graph_groupbox_layout)
    #     self._centralLayout.addWidget(graph_groupbox)

    #     self.input_func = QLineEdit()
    #     self.graph_groupbox_layout.addWidget(self.input_func)
    #     self.input_func.setText("2*t + 1")

    #     self._plot_graph()

    #     draw_button = QPushButton("Draw")
    #     draw_button.clicked.connect(self._draw_button)
    #     self.graph_groupbox_layout.addWidget(draw_button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FourierManGui()
    win.show()
    sys.exit(app.exec_())