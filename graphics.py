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
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import threading
import time

dir_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前路径
sys.path.append(dir_path+'/view')  # ui视图层
# from Ui_serial import Ui_MainWindow
from Ui_graphics import Ui_Form

class GraphicsView(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("俊杰绘图高手")
        # height = self.graphi height()
        # width = self.width()
        self.graphics()
        self.graphicsView.scale(1,-1) # 倒转
        self.timer =QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timer.start(1000)
        # self.animation()
        


    def graphics(self, newPos = [0,0]):
        # h = self.graphicsView.height()-20
        # w = self.graphicsView.width()-20
        h = 500
        w = 7505/10
        
        # self.rect = QRectF(0,0,w-10,h-10)
        # self.scene = QGraphicsScene(self.rect)
        self.scene = QGraphicsScene()

        self.graphicsView.setScene(self.scene)
        
        
        self.scene.addRect(0,0,w,h)

        self.scene.addEllipse(0,0,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(0,h,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(w,0,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(w,h,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))

        self.scene.addLine(0,0,w,0, pen = QPen(QColor.fromRgb(255, 0, 0)))
        self.scene.addLine(0,0,0,h, pen = QPen(QColor.fromRgb(255, 0, 0)))

        # self.scene.addRect(0,0,100,100)
        # self.scene.addRect(102,0,100,100)
        # self.scene.addRect(0,102,100,100)
        # self.scene.addRect(102,102,100,100)


        self.anchor_0 = np.array([0, 0], dtype=np.int64)
        self.anchor_1 = np.array([w, 0], dtype=np.int64)
        self.anchor_2 = np.array([0, h], dtype=np.int64)

        brick_width = 1000/10  # 砖长：300mm
        brick_height = 1000/10
        self.brick_gap = 50/10  # 砖间隙：5mm

        global height_num, width_num
        height_num = np.int(self.anchor_2[1]/brick_height)
        width_num = np.int(self.anchor_1[0]/brick_width)

        global bricks  # 全局
        bricks = np.zeros((width_num*height_num, 5), dtype=int)  # 可利用json数据类型

        """ 砖摆放，从x,y轴出发 """
        for j in range(height_num):
            for i in range(width_num):

                self.brick_x = i*(self.brick_gap+brick_width)
                self.brick_y = j*(self.brick_gap+brick_height)

                bricks[i+j] = [i, j, self.brick_x,
                               self.brick_y, 0]  # 填写每一块砖的信息
                # print(bricks[i+j])

                rectangle_item = QGraphicsRectItem(self.brick_x, self.brick_y, brick_width, brick_height)
                # Add the patch to the Axes
                # currentAxis.add_patch(self.rectangle)
                self.scene.addItem(rectangle_item)


        # self.graphicsView.scale(1,1.5)
        # self.scene.removeItem(item1)

    def animation(self):
        # h = self.graphicsView.height()-20
        # w = self.graphicsView.width()-20
        h = 500
        w = 7505/10
        
        self.rect = QRectF(0,0,w-10,h-10)
        self.scene = QGraphicsScene(self.rect)
        # self.scene = QGraphicsScene()

        self.graphicsView.setScene(self.scene)
        # self.graphicsView.setSceneRect(-180, -90, 360, 180)
        
        
        
        self.scene.addRect(0,0,w,h)

        self.scene.addEllipse(0,0,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(0,h,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(w,0,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(w,h,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))

        self.scene.addLine(0,0,w,0, pen = QPen(QColor.fromRgb(255, 0, 0)))
        self.scene.addLine(0,0,0,h, pen = QPen(QColor.fromRgb(255, 0, 0)))

        self.anchor_0 = np.array([0, 0], dtype=np.int64)
        self.anchor_1 = np.array([w, 0], dtype=np.int64)
        self.anchor_2 = np.array([0, h], dtype=np.int64)

        brick_width = 1000/10  # 砖长：300mm
        brick_height = 1000/10
        self.brick_gap = 50/10  # 砖间隙：5mm

        global height_num, width_num
        height_num = np.int(self.anchor_2[1]/brick_height)
        width_num = np.int(self.anchor_1[0]/brick_width)

        global bricks  # 全局
        bricks = np.zeros((width_num*height_num, 5), dtype=int)  # 可利用json数据类型

        """ 砖摆放，从x,y轴出发 """
        for j in range(height_num):
            for i in range(width_num):

                self.brick_x = i*(self.brick_gap+brick_width)
                self.brick_y = j*(self.brick_gap+brick_height)

                bricks[i+j] = [i, j, self.brick_x,
                               self.brick_y, 0]  # 填写每一块砖的信息
                # print(bricks[i+j])

                rectangle_item = QGraphicsRectItem(self.brick_x, self.brick_y, brick_width, brick_height)
                # Add the patch to the Axes
                # currentAxis.add_patch(self.rectangle)
                self.scene.addItem(rectangle_item)

        x = np.random.rand(1) *500
        y = np.random.rand(1)*500
        
        newPos = [x, y]
        # self.graphics(newPos) 
        print("x:%f"%newPos[0] + ", y:%f"%newPos[1])
        # self.scene.addEllipse(newPos[0], newPos[1],10,10)

        item = QGraphicsEllipseItem(newPos[0], newPos[1], 15, 15)
        item.setBrush(QBrush(QColor.fromRgb(0, 255, 255)))
        self.scene.addItem(item)


    def wheelEvent(self, event):
        """
        Zoom in or out of the view.
        """
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.graphicsView.mapToScene(event.pos())
        # print("oldPos：%d" %oldPos[0])

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.graphicsView.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.graphicsView.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.graphicsView.translate(delta.x(), delta.y())
       
    def mousePressEvent(self, event):
        """ 都是函数名改写 """
        # print("xixixi1")
        if event.button() == Qt.RightButton:
            print("right")
        elif event.button() == Qt.LeftButton:
            print("left")
        elif event.button() == Qt.MidButton:
            print("mid")
        
        oldPos = event.pos()
        print("old x:%d"%oldPos.x() + ", old y:%d"%oldPos.y())

        
    def mouseReleaseEvent(self, event):
        newPos = event.pos()
        print("new x:%d"%newPos.x() + ", new y:%d"%newPos.y())

    def mouseMoveEvent(self, event):
        print("hahaasdas")
    
    # def axis_location(self):





    
if __name__ == '__main__':
    graphics_app = QtWidgets.QApplication(sys.argv)

    graphics_form = GraphicsView()
    graphics_form.show()

    sys.exc_info(graphics_app.exec_())