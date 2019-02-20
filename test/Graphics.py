import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

dir_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前路径
sys.path.append(dir_path + '/view')

from Ui_graphics import Ui_Form


class Graphics_From(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(Graphics_From, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("绘图")
        self.init()
        # self.graphicsView.leftMouseButtonPressed.connect(self.function())
        
    
    def function(self):
        print("heheheh")
    
    def init(self):
        scene = QGraphicsScene()
        
        redBrush = QBrush(Qt.red)
        blueBrush = QBrush(Qt.blue)
        blackPen = QPen(Qt.black)
        blackPen.setWidth(7)


        ellipse = scene.addEllipse(10,10,200,200,blackPen,redBrush)
        rectange = scene.addRect(-100,-100,200,200,blackPen,blueBrush)

        ellipse.setFlag(QGraphicsItem.ItemIsMovable) #使图像可移动
        rectange.setFlag(QGraphicsItem.ItemIsMovable)

        self.graphicsView.setScene(scene)
        self.graphicsView.scale(1.2,-1.2)


if __name__ == "__main__":
    graphics_app = QtWidgets.QApplication(sys.argv)
    graphics_form = Graphics_From()
    graphics_form.show()
    sys.exit(graphics_app.exec_())  