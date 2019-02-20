from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Matplotlib Emdding In Pyqt5"
        top = 400
        left = 400
        width = 900
        height = 500

        self.setWindowTitle(title)
        self.setGeometry(top,left,width,height)

        self.MyUi()
    
    def MyUi(self):
        canvas = Canvas(self, width = 8,height=4)
        canvas.move(0,0)

        button = QPushButton("click me",self)
        button.move(100,450)

        butto2 = QPushButton("click me",self)
        butto2.move(200,450)
        
class Canvas(FigureCanvas):
    def __init__(self,parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width,height),dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
    
    def plot(self):
        x = np.array([50,30,40])
        labels = ["Apple","Banana","Melons"]
        ax = self.figure.add_subplot(111)
        




app = QApplication(sys.argv)
Window = Window()
Window.show()
app.exec()