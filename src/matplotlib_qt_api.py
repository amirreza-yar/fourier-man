# THIS THE FILE CONTAIN THE GRAPH OBJECT AND WILL BE USED AS AN API, USING MATPLOTLIB
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# CREATIGN THE MATPLOTLIB API CLASS TO WORK ON PYPLOT SYS
class PltCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100) -> None:
        # SETTING THE FIGURE INSTANCE
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(PltCanvas, self).__init__(self.fig)