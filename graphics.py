import sys
import numpy as np
import random
import os
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QObject, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor


dir_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前路径
sys.path.append(dir_path+'/view')  # ui视图层
# from Ui_serial import Ui_MainWindow
from Ui_graphics import Ui_Form


class SimpleWindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("俊杰绘图高手")
        global h, w 
        h = 500
        w = 750

        self.init()
        self.graphics()
        self.graphicsView.scale(1, -1)  # 倒转

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animation)
        self.timer.start(200)

    def init(self):
        self.rect = QRectF(0, 0, w, h)
        global scene
        scene = QGraphicsScene(self.rect)
        # scene = QGraphicsScene()

        self.graphicsView.setScene(scene)

        scene.addRect(0, 0, w, h)

        # 画坐标系的四个顶点
        ellipse_brush = QBrush(QColor.fromRgb(120, 50, 255))
        scene.addEllipse(
            0-8, 0-8, 15, 15, brush=ellipse_brush)
        scene.addEllipse(
            0-8, h-8, 15, 15, brush=ellipse_brush)
        scene.addEllipse(
            w-8, 0-8, 15, 15, brush=ellipse_brush)
        scene.addEllipse(
            w-8, h-8, 15, 15, brush=ellipse_brush)

        # 画出x, y 轴
        scene.addLine(0, 0, w, 0, pen=QPen(Qt.red))
        scene.addLine(0, 0, 0, h, pen=QPen(Qt.red))

        # 三个基站的位置
        self.anchor_0 = np.array([0, 0], dtype=np.int64)
        self.anchor_1 = np.array([w, 0], dtype=np.int64)
        self.anchor_2 = np.array([0, h], dtype=np.int64)

        global brick_width, brick_height
        brick_width = 1000/10  # 砖长：300mm
        brick_height = 1000/10
        self.brick_gap = 50/10  # 砖间隙：5mm

        global height_num, width_num
        height_num = np.int(self.anchor_2[1]/brick_height)
        width_num = np.int(self.anchor_1[0]/brick_width)

        # 画出机器人位置
        x = np.random.rand(1)*500
        y = np.random.rand(1)*500
        robotPos = [x, y]
        item = QGraphicsEllipseItem(robotPos[0], robotPos[1], 10, 10)
        item.setBrush(QBrush(QColor.fromRgb(0, 255, 255)))
        scene.addItem(item)

        return robotPos



    def graphics(self):
        self.init()

        global bricks  # 全局
        bricks = np.zeros((width_num*height_num, 5), dtype=int)  # 可利用json数据类型

        """ 砖摆放，从x,y轴出发 """
        for j in range(height_num):
            for i in range(width_num):

                self.brick_x = i*(self.brick_gap+brick_width)
                self.brick_y = j*(self.brick_gap+brick_height)

                bricks[j * width_num + i] = [i, j, self.brick_x,
                               self.brick_y, 0]  # 填写每一块砖的信息

                rectangle_item = QGraphicsRectItem(
                    self.brick_x, self.brick_y, brick_width, brick_height)
                
                scene.addItem(rectangle_item)


    def animation(self):
        robotPos = self.init()
       
        """ 砖摆放，从x,y轴出发 """
        for j in range(height_num):
            for i in range(width_num):

                self.brick_x = i*(self.brick_gap+brick_width)
                self.brick_y = j*(self.brick_gap+brick_height)

                rectangle_item = QGraphicsRectItem(
                    self.brick_x, self.brick_y, brick_width, brick_height)
                
                scene.addItem(rectangle_item)

        print(bricks)
        print("x：%f" % robotPos[0] + "，y：%f" % robotPos[1])
        
        # rectangle_item = QGraphicsRectItem(
        #             bricks[10][2], bricks[10][3], brick_width, brick_height)
        # rectangle_item.setBrush(Qt.blue) # item set color
        # scene.addItem(rectangle_item)

        # 动态画出铺砖的轨迹
        red_brush = QBrush(QColor.fromRgb(255, 0, 0))
        white_brush = QBrush(QColor.fromRgb(255,255,255))
        for k in range(height_num * width_num):
            if robotPos[0] >= bricks[k][2] and robotPos[0] <= bricks[k][2] + brick_width and robotPos[1] >= bricks[k][3] and robotPos[1] <= bricks[k][3] + brick_height:
                bricks[k][4] = 1
            # else:
            #     bricks[k][4] = 0

        for brick in bricks:  # 铺完一块砖就覆盖颜色
            if brick[4] == 1:
                scene.addRect(brick[2], brick[3], brick_width, brick_height, brush = red_brush)    
            else:
                scene.addRect(brick[2], brick[3], brick_width, brick_height, brush = white_brush)    
            scene.addRect(0, 0, w, h) # 一定要画出最外的矩形区域
            

        robot_item = QGraphicsEllipseItem(robotPos[0], robotPos[1], 10, 10)
        robot_item.setBrush(QBrush(QColor.fromRgb(0, 255, 255)))
        scene.addItem(robot_item)


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

    # def mousePressEvent(self, event):
    #     """ 都是函数名改写 """
    #     # print("xixixi1")
    #     if event.button() == Qt.RightButton:
    #         print("right")
    #     elif event.button() == Qt.LeftButton:
    #         print("left")
    #     elif event.button() == Qt.MidButton:
    #         print("mid")

    #     oldPos = event.pos()
    #     print("old x:%d"%oldPos.x() + ", old y:%d"%oldPos.y())

    # def mouseReleaseEvent(self, event):
    #     newPos = event.pos()
    #     print("new x:%d"%newPos.x() + ", new y:%d"%newPos.y())

    def mouseMoveEvent(self, event):
        # self.graphicsView.setCursor(Qt.CrossCursor)
        # self.graphicsView.setMouseTracking(True)
        # self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        newPos = event.pos()
        print("mouseMoveEvent->x:%d" % newPos.x())


if __name__ == '__main__':
    graphics_app = QtWidgets.QApplication(sys.argv)

    graphics_form = SimpleWindow()
    graphics_form.show()

    sys.exc_info(graphics_app.exec_())
