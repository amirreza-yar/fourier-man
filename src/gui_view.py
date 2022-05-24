# IMPORTING THE NEEDED MODULES FROM PYAT5 AND NUMPY
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QGroupBox, QLineEdit, QTableWidget,
    QHeaderView, QSizePolicy, QAbstractScrollArea, QMenuBar, QMenu, QAction, qApp, QStyle, QLabel
)
from PyQt5.QtGui import QIcon
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

        # CREATING DIFFRENT PARTS OF MAIN WINDOW
        self._createInputSection()
        self._createGraphSection()
        self._createMenubar()
        self._createStatusBar()
        self._createControlMenu()

    def _createControlMenu(self):
        #TODO SHOULD HAVE CONTROLS TO MANIPULATE GRAPH DATA
        pass

    def _createStatusBar(self):
        #TODO ADD A TERMINATE TASK OPERATOR
        #TODO SHOW ERRORS IN RED COLOR
        self._statusBar = self.statusBar()
        self._statusBar.showMessage("Ready", 5000)
        # self._statusBar.addPermanentWidget(QPushButton("Terminate"))

    def _createInputSection(self):
        inputGroupBox, inputGroupBoxLayout = self._createInputGroupBox()
        self._centralLayout.addWidget(inputGroupBox)

        # ADDING FUNCTION TABLE
        inputGroupBoxLayout.addWidget(self._createInputTable())
        # ADDING PLOT NEW FUNCTION BUTTON
        #TODO CAN BE MOVED TO A DIFFRENT SECTION AND HAVE A SHORTCUT
        inputGroupBoxLayout.addWidget(self._createDrawButton())

        #TODO MUST ADD A TIME PERIOD PART
        #TODO MUST ADD A INTEGRATION'S BOUNDARY

    def _createInputGroupBox(self):
        inputGroupBox = QGroupBox("Input Section")
        inputGroupBoxLayout = QVBoxLayout()
        inputGroupBox.setLayout(inputGroupBoxLayout)
        inputGroupBox.setSizePolicy(self._stretchSizePolicy(2))
        inputGroupBox.setMinimumSize(250, 350)
        return inputGroupBox, inputGroupBoxLayout
        

    def _createMenubar(self):
        #TODO ORGANIZE THIS PART
        #TODO SHOULD HAVE OPEN/SAVE METHOD TO CONTROL FILES AND USE THEM LATER
        #TODO SHOULD ADD A MENU TO CHANGE ALGORITHEM PREFFRENCES
        menuBar = self.menuBar()
        # Using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Using a title
        editMenu = menuBar.addMenu("&Edit")
        # Using an icon and a title
        helpMenu = menuBar.addMenu("&Help")
        
        
        self.newAction = QAction(self)
        self.newAction.setText("&New")
        # self.newAction.setIcon()
        self.openAction = QAction(QIcon(":file-open.svg"), "&Open...", self)
        self.saveAction = QAction(QIcon(":file-save.svg"), "&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.exitAction.setShortcut("Ctrl+q")

        self.exitAction.triggered.connect(self.exitTrigger)

        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

    def exitTrigger(self):
        # INSTANCE TRIGGER
        #TODO SHOULD MOVE TRIGGER FUNCTIONS TO A DIFFRENT FILE
        exit(1)

    def _createInputTable(self):
        self.inputTable = QTableWidget(3, 2)
        self.inputTable.setHorizontalHeaderLabels(["Function", "Boundary"])
        tableHorHeader = self.inputTable.horizontalHeader()
        tableHorHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        tableHorHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        #TODO SHOULD CHECK NEXT LINE
        # self.inputTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        return self.inputTable

    def _createGraphSection(self):
        #TODO SHOULD ADD BASE GRAPH
        graphGroupBox = QGroupBox("Graph Section")
        graphGroupBoxLayout = QVBoxLayout()
        graphGroupBox.setSizePolicy(self._stretchSizePolicy(3))
        graphGroupBox.setMinimumSize(400, 350)
        graphGroupBox.setLayout(graphGroupBoxLayout)
        graphGroupBoxLayout.addWidget(self._createGraph())
        self._centralLayout.addWidget(graphGroupBox)

    def _findSeries(self, time = 0):
        #TODO SHOULD ADD A VALIDATOR PART TO CATCH ERRORS
        myfunction = FourierSeries(3, -1, 2, 5, "2*t + 1")
        return myfunction.xt(time)

    def _stretchSizePolicy(self, horNum = 1, verNum = None):
        # A FUNCTION TO RESIZE WIDGETS EASIER
        #TODO CAN BE A SEPERATE PYTHONIC CLASS
        widgetSizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        widgetSizePolicy.setHorizontalStretch(horNum)
        if verNum:
            widgetSizePolicy.setVerticalStretch(verNum)
        return widgetSizePolicy

    def _createDrawButton(self):
        drawButton = QPushButton("Draw")
        drawButton.clicked.connect(self._drawNewGraph)
        return drawButton

    def _drawNewGraph(self):
        #TODO SHOULD HAVE A SHORTCUT
        self.xtFig.canvas.flush_events()
        time = np.linspace(-5, 5, 500)
        newSeries = self._findSeries(time)
        self.ax1.set_ylim ([np.min(newSeries) - 0.2, np.max(newSeries) + 0.2])
        self.line1.set_ydata(newSeries)
        self.xtFig.canvas.draw()

    def _createGraph(self):
        xtGraph = PltCanvas()
        time = np.linspace(-5, 5, 500)
        self.xtFig = xtGraph.fig
        self.ax1 = self.xtFig.add_subplot(111)
        xtData = self._findSeries(time)
        self.ax1.set_ylim ([np.min(xtData) - 0.2, np.max(xtData) + 0.2])
        self.line1, = self.ax1.plot(time, xtData, 'r-')
        return xtGraph

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FourierManGui()
    win.show()
    sys.exit(app.exec_())