# IMPORTING THE NEEDED MODULES FROM PYAT5, NUMPY, MATPLOTLIB, SYS
import time
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QGroupBox, QLineEdit, QTableWidget,
    QHeaderView, QSizePolicy, QAbstractScrollArea, QMenuBar, QMenu, QAction, qApp, QStyle, QLabel, QTableWidgetItem
)
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import sys
from ast import literal_eval
from functools import partial

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
        self._createLeftSide()
        self._createGraphSection()
        self._createMenubar()
        self._createStatusBar()

    def _createStatusBar(self):
        self._statusBar = self.statusBar()
        self._statusBar.showMessage("Ready", 5000)
        #TODO ADD A TERMINATE TASK OPERATOR
        #TODO SHOW ERRORS IN RED COLOR

    def _createLeftSide(self):
        leftSideLayout = QVBoxLayout()
        leftSideLayout.addWidget(self._createInputSection())
        leftSideLayout.addWidget(self._createGraphControlSection())
        leftSideLayout.addWidget(self._createDrawButton())
        self._centralLayout.addLayout(leftSideLayout)


    def _createInputSection(self):
        inputGroupBox, inputGroupBoxLayout = self._createInputGroupBox()
        # ADDING FUNCTION TABLE
        inputGroupBoxLayout.addWidget(self._createInputTable())
        inputGroupBoxLayout.addLayout(self._createTimePeriodLineEdit())
        inputGroupBoxLayout.addLayout(self._createIntegralBoundaiesLineEdit())
        return inputGroupBox
        #TODO ADD HARMONY PART

    def _createGraphControlSection(self):
        graphControlGroupBox = QGroupBox("Graph Control Section")
        graphControlGroupBoxLayout = QHBoxLayout()
        graphControlGroupBox.setLayout(graphControlGroupBoxLayout)
        leftSideControl = QVBoxLayout()
        graphControlGroupBoxLayout.addLayout(leftSideControl)
        rightSideControl = QVBoxLayout()
        graphControlGroupBoxLayout.addLayout(rightSideControl)

        leftSideControl.addWidget(QCheckBox("Grid"))
        rightSideControl.addWidget(QCheckBox("Base Function Graph"))
        return graphControlGroupBox
        #TODO ADD HARMONY CHANGER TO THIS PART
        #TODO ADD CHANGE GRAPH VIEW HOR TO VER OR REVERSE
        #TODO SHOULD HAVE CHANGE RAPH COLOR PART
        #TODO ADD XLIM AND YLIM PART
        
    def _createGraphControlGroupBox(self):
        graphControlGroupBox = QGroupBox("Graph Control Section")
        graphControlGroupBoxLayout = QHBoxLayout()
        graphControlGroupBox.setLayout(graphControlGroupBoxLayout)
        return graphControlGroupBox, graphControlGroupBoxLayout

    
    def _createIntegralBoundaiesLineEdit(self):
        integralBoundariesLayout = QHBoxLayout()
        integralBoundariesLayout.addWidget(QLabel("Integration boundaries are from"))
        self.integrationLowerBound = QLineEdit()
        integralBoundariesLayout.addWidget(self.integrationLowerBound)
        integralBoundariesLayout.addWidget(QLabel("to"))
        self.integrationUpperBound = QLineEdit()
        integralBoundariesLayout.addWidget(self.integrationUpperBound)
        return integralBoundariesLayout
    
    def _createTimePeriodLineEdit(self):
        timePriodLayout = QHBoxLayout()
        timePriodLayout.addWidget(QLabel("Time period is "))
        self.timePriod = QLineEdit()
        timePriodLayout.addWidget(self.timePriod)
        return timePriodLayout

    def _createInputGroupBox(self):
        inputGroupBox = QGroupBox("Input Section")
        inputGroupBoxLayout = QVBoxLayout()
        inputGroupBox.setLayout(inputGroupBoxLayout)
        inputGroupBox.setSizePolicy(self._stretchSizePolicy(2))
        inputGroupBox.setMinimumSize(250, 350)
        inputGroupBox.setMaximumWidth(350)
        return inputGroupBox, inputGroupBoxLayout
        

    def _createMenubar(self):
        
        # CONSTRUCTING MENU BAR ITEMS
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("&File")
        self._menuActionCreator(fileMenu, {
            "&New": ["Ctrl+n", None],
            "&Open...": ["Ctrl+o", None],
            "&Save": ["Ctrl+s", "SP_DialogSaveButton"],
            "&Export": ["Ctrl+Shit+e", None, True],
            "&Exit": ["Ctrl+q", "SP_DialogCloseButton"],
        })

        preferencesMenu = menuBar.addMenu("&Preferences")
        self._menuActionCreator(preferencesMenu, {
            "&Manipulate graph": "Ctrl+e",
            "&Matplotlib graph editor": "Ctrl+Shift+e",
        })
        helpMenu = menuBar.addMenu("&Help")
        self._menuActionCreator(helpMenu, {
            "&Info": None,
            "&Docs": None,
            "&Tutorials": None,
            "&Source Files": None,
            "&About Association": None,
        })
        #TODO FILE HELP SHOULD HAVE WRITER INFO, DOCS, TUTORIALS, GITHUB REPO, ABOUT ASSOCIATIONS
        #TODO SHOULD HAVE OPEN/SAVE METHOD TO CONTROL FILES AND USE THEM LATER
    
    def _menuActionCreator(self, menuName, actions:dict):
        for key in actions:
            if type(actions[key]) is list:
                shortcut = actions[key][0]
                icon = actions[key][1]
            else:
                shortcut = actions[key]
                icon = None
            # print(key, shortcut)
            newAction = QAction(key, self)
            if shortcut:
                newAction.setShortcut(shortcut)
            if icon:
                # print(key, icon)
                newAction.setIcon(self._createIcon(icon))
            menuName.addAction(newAction)
            try:
                haveSeperator = actions[key][2]
                if haveSeperator:
                    menuName.addSeparator()
            except:
                pass


    def _createIcon(self, iconName:str):
        return self.style().standardIcon(getattr(QStyle, iconName))
    
    def exitTrigger(self):
        # INSTANCE TRIGGER
        exit(1)

    def _createInputTable(self):
        self.inputTable = QTableWidget(1, 2)
        self.inputTable.setHorizontalHeaderLabels(["Function", "Boundary"])
        tableHorHeader = self.inputTable.horizontalHeader()
        tableHorHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        tableHorHeader.setSectionResizeMode(1, QHeaderView.Stretch)
        #TODO SHOULD CHECK NEXT LINE
        # self.inputTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.inputTable.cellChanged.connect(self._addNewTableRowTrigger)
        self.inputTable.setItem(0, 0, QTableWidgetItem())
        self.inputTable.setItem(0, 1, QTableWidgetItem())
        self.inputTable.item(0, 0).setText("2*t + 1")
        self.inputTable.item(0, 1).setText("t>0")
        return self.inputTable
        #TODO SHOULD MOVE TRIGGER FUNCTIONS TO A DIFFRENT FILE
    
    def _addNewTableRowTrigger(self, row):
        rowCount = self.inputTable.rowCount()
        if row == rowCount-1:
            self.inputTable.insertRow(rowCount)

    def _createGraphSection(self):
        graphGroupBox = QGroupBox("Graph Section")
        graphGroupBoxLayout = QVBoxLayout()
        graphGroupBox.setSizePolicy(self._stretchSizePolicy(3))
        graphGroupBox.setMinimumSize(400, 350)
        graphGroupBox.setLayout(graphGroupBoxLayout)
        graphGroupBoxLayout.addWidget(self._createGraph())
        self._centralLayout.addWidget(graphGroupBox)
        #TODO SHOULD ADD BASE GRAPH

    def _evaluateTableFunction(self):
        rowCount = self.inputTable.rowCount()
        strFunctionsList = list()
        boundarysList = list()
        for row in range(rowCount):
            functionCell = self.inputTable.item(row, 0)
            boundaryCell = self.inputTable.item(row, 1)
            if functionCell and boundaryCell:
                strFunctionsList.append(functionCell.text())
                boundarysList.append(boundaryCell.text())

        # THIS FUNCTION CONVERT PYTHONIC AND OPERATOR TO NUMPY AND OPERATOR
        def correctAndOp(boundaries):
            boundaryStr = str()
            for boundaryNum in range(len(boundaries)):
                if boundaryNum == 0:
                    boundaryStr += f"({boundaries[boundaryNum]})"
                else:
                    boundaryStr += f"*({boundaries[boundaryNum]})"
            return boundaryStr

        # EVALUATING THE INPUT FUNCTIONS TO PYTHON EXPRESSIONS
        functionsList = [eval("lambda t: " + func) for func in strFunctionsList]
        # EVALUATING THE INPUT BOUNDARIES TO NUMPY EXPRESSIONS
        boundArray = list()
        for boundary in boundarysList:
            if 'and' in boundary:
                andBound = boundary.split('and')
                boundArray.append(correctAndOp(andBound))
            elif '&' in boundary:
                andBound = boundary.split('&')
                boundArray.append(correctAndOp(andBound))
            else:
                boundArray.append(boundary)

        return lambda t: np.piecewise (t, [eval(bond, {}, {"t": t}) for bond in boundArray], functionsList)

    def _findSeries(self, time = 0):
        myfunction = FourierSeries(2, -1, 1, 300, self._evaluateTableFunction())
        return myfunction.xt(time)
        #TODO SHOULD ADD A VALIDATOR PART TO CATCH ERRORS

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
        drawButton.setShortcut("Ctrl+Return")
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
        self._evaluateTableFunction()
    


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