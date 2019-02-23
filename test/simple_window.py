import sys
import numpy as np
import random
import os
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtWidgets import QMessageBox, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QObject,QRectF
from PyQt5.QtGui import QBrush, QPen, QColor

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(-100, -100, 200, 200)
        self.opt = ""

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        pen = QPen(QtCore.Qt.black)
        brush = QBrush(QtCore.Qt.black)
        x = event.scenePos().x()
        y = event.scenePos().y()
        if self.opt == "Generate":
            self.addEllipse(x, y, 4, 4, pen, brush)
        elif self.opt == "Select":
            print(x, y)


class SimpleWindow(QtWidgets.QMainWindow, points.Ui_Dialog):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)
        self.setupUi(self)

        self.scene = GraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        group = QButtonGroup(self)
        group.addButton(self.radioButton)
        group.addButton(self.radioButton_2)

        group.buttonClicked.connect(lambda btn: self.scene.setOption(btn.text()))
        self.radioButton.setChecked(True)
        self.scene.setOption(self.radioButton.text())


if __name__ == '__main__':
    graphics_app = QtWidgets.QApplication(sys.argv)

    graphics_form = SimpleWindow()
    graphics_form.show()

    sys.exc_info(graphics_app.exec_())