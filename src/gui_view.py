# IMPORTING THE NEEDED MODULES FROM PYAT5, NUMPY, SYS
import time
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QGroupBox, QLineEdit, QTableWidget,
    QHeaderView, QSizePolicy, QAbstractScrollArea, QMenuBar, QMenu, QAction, qApp, QStyle, QLabel, QTableWidgetItem
)
from PyQt5.QtGui import QIcon
import numpy as np
import sys
from functools import partial

# IMPORTING THE LOCAL MODULES
from .fourier_series_model import FourierSeries
from .matplotlib_qt_api import PltCanvas

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
        inputGroupBoxLayout.addLayout(self._createTime())
        inputGroupBoxLayout.addLayout(self._createTimePeriodLineEdit())
        inputGroupBoxLayout.addLayout(self._createIntegralBoundaiesLineEdit())
        inputGroupBoxLayout.addLayout(self._createHarmonicLineEdit())
        return inputGroupBox
        #TODO ADD HARMONY PART

    def _createInputGroupBox(self):
        inputGroupBox = QGroupBox("Input Section")
        inputGroupBoxLayout = QVBoxLayout()
        inputGroupBox.setLayout(inputGroupBoxLayout)
        inputGroupBox.setSizePolicy(self._stretchSizePolicy(2))
        inputGroupBox.setMinimumSize(250, 350)
        inputGroupBox.setMaximumWidth(350)
        return inputGroupBox, inputGroupBoxLayout
    
    def _createTime(self):
        timeLayout = QHBoxLayout()
        timeLayout.addWidget(QLabel("Time is"))
        self.timeLowerBound = QLineEdit()
        self.timeLowerBound.setText("-5")
        timeLayout.addWidget(self.timeLowerBound)
        timeLayout.addWidget(QLabel("to"))
        self.timeUpperBound = QLineEdit()
        self.timeUpperBound.setText("5")
        timeLayout.addWidget(self.timeUpperBound)
        timeLayout.addWidget(QLabel("with"))
        self.timeSamples = QLineEdit()
        self.timeSamples.setText("500")
        timeLayout.addWidget(self.timeSamples)
        timeLayout.addWidget(QLabel("samples"))
        self.time = np.linspace(int(self.timeLowerBound.text()),
                                int(self.timeUpperBound.text()), 
                                int(self.timeSamples.text()))
        return timeLayout

    def _createTimePeriodLineEdit(self):
        timePriodLayout = QHBoxLayout()
        timePriodLayout.addWidget(QLabel("Time period is "))
        self.timePeriod = QLineEdit()
        self.timePeriod.setText("2")
        timePriodLayout.addWidget(self.timePeriod)
        return timePriodLayout

    def _createIntegralBoundaiesLineEdit(self):
        integralBoundariesLayout = QHBoxLayout()
        integralBoundariesLayout.addWidget(QLabel("Integration boundaries are from"))
        self.integrationLowerBound = QLineEdit()
        self.integrationLowerBound.setText("-1")
        integralBoundariesLayout.addWidget(self.integrationLowerBound)
        integralBoundariesLayout.addWidget(QLabel("to"))
        self.integrationUpperBound = QLineEdit()
        self.integrationUpperBound.setText("1")
        integralBoundariesLayout.addWidget(self.integrationUpperBound)
        return integralBoundariesLayout

    def _createHarmonicLineEdit(self):
        harmonicLayout = QHBoxLayout()
        harmonicLayout.addWidget(QLabel("Harmonic is "))
        self.harmonic = QLineEdit()
        self.harmonic.setText("10")
        harmonicLayout.addWidget(self.harmonic)
        return harmonicLayout

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
        #TODO SHOULD HAVE CHANGE GRAPH COLOR PART
        #TODO ADD XLIM AND YLIM PART
        
    def _createGraphControlGroupBox(self):
        graphControlGroupBox = QGroupBox("Graph Control Section")
        graphControlGroupBoxLayout = QHBoxLayout()
        graphControlGroupBox.setLayout(graphControlGroupBoxLayout)
        return graphControlGroupBox, graphControlGroupBoxLayout

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
        #TODO SHOULD MOVE self.inputTable.cellChanged.connect(self._addNewTableRowTrigger) TO CONTROLS
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
        T = int(self.timePeriod.text())
        T1 = int(self.integrationLowerBound.text())
        T2 = int(self.integrationUpperBound.text())
        harmonic = int(self.harmonic.text())
        myfunction = FourierSeries(T, T1, T2, harmonic, self._evaluateTableFunction())
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
        drawButton.setShortcut("Ctrl+D")
        return drawButton

    def _drawNewGraph(self):
        self.xtFig.canvas.flush_events()
        self.time = np.linspace(int(self.timeLowerBound.text()),
                                int(self.timeUpperBound.text()), 
                                int(self.timeSamples.text()))
        newSeries = self._findSeries(self.time)
        self.ax1.set_xlim([np.min(self.time) - 0.2, np.max(self.time) + 0.2])
        self.ax1.set_ylim([np.min(newSeries) - 0.2, np.max(newSeries) + 0.2])
        self.line1.set_ydata(newSeries)
        self.xtFig.canvas.draw()
        self._evaluateTableFunction()

    def _createGraph(self):
        xtGraph = PltCanvas()
        self.xtFig = xtGraph.fig
        self.ax1 = self.xtFig.add_subplot(111)
        xtData = self._findSeries(self.time)
        self.ax1.set_ylim ([np.min(xtData) - 0.2, np.max(xtData) + 0.2])
        self.line1, = self.ax1.plot(self.time, xtData, 'r-')
        return xtGraph

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = FourierManGui()
#     win.show()
#     sys.exit(app.exec_())