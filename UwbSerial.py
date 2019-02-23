import sys
import numpy as np
import random
import os
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QObject,QRectF
from PyQt5.QtGui import QBrush, QPen, QColor
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


dir_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前路径
sys.path.append(dir_path+'/view')  # ui视图层
# from Ui_serial import Ui_MainWindow
from Ui_serial import Ui_MainWindow


class Pyqt5_Serial(QtWidgets.QMainWindow, Ui_MainWindow):
      # 声明信号
    serial_signal = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(Pyqt5_Serial, self).__init__(parent=parent)
        self.setupUi(self)
        self.init()
        self.setWindowTitle("UWB串口助手")
        self.serial_uwb = serial.Serial()
        self.port_check()

        otherClass = MyDynamicMplCanvas()  # 信号和槽，传送数据给QDialoge
        self.serial_signal.connect(otherClass.robot_position)
        self.serial_signal.emit(0, 0)

        self.graphicsView.scale(1,-1) # x轴倒转
        self.graphics()
        

    def init(self):
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)
        # 串口信息显示
        # self.s1__box_2.currentTextChanged.connect(self.port_info)
        # 打开串口按钮
        self.open_serial_button.clicked.connect(self.port_open)
        # 关闭串口按钮
        self.close_serial_button.clicked.connect(self.port_close)
        # 接受数据定时器
        self.timer_receive = QTimer(self)
        self.timer_receive.timeout.connect(self.data_receive)

    def port_check(self):
        """ 检测所有串口 """
        self.Com_Dict = {}  # 将所有串口信息存储在字典中
        port_list = list(serial.tools.list_ports.comports())
        self.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.s1__box_2.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.open_serial_button.setEnabled(False)

    def port_open(self):
        """ 打开串口 """
        # self.serial_uwb.port = "COM3"  #串口号
        self.serial_uwb.port = self.s1__box_2.currentText()
        self.serial_uwb.baudrate = int(115200)  # 波特率
        self.serial_uwb.bytesize = int(8)  # 数据位
        self.serial_uwb.parity = "N"  # 奇偶性，即校验位
        self.serial_uwb.stopbits = int(1)  # 停止位

        # sudo chmod a+rw /dev/ttyACM0 给予权限

        try:
            self.serial_uwb.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer_receive.start(200)

        if self.serial_uwb.isOpen():
            self.open_serial_button.setEnabled(False)
            self.close_serial_button.setEnabled(True)

    def port_close(self):
        """ 关闭串口 """
        self.timer_receive.stop()
        try:
            self.serial_uwb.close()
        except:
            pass
        self.open_serial_button.setEnabled(True)
        self.close_serial_button.setEnabled(False)

    def data_receive(self):

        otherClass = MyDynamicMplCanvas()  # 信号和槽，传送数据给QDialoge

        """ 数据接收 """
        try:
            num = self.serial_uwb.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            serial_data = self.serial_uwb.read(num)
            unicode_data = serial_data.decode('iso-8859-1')
            # print(unicode_data)
            # return unicode_data

            data_lines = unicode_data.split('\r\n')  # 列表

            for line in data_lines:
                data = line.split()
                if len(data) == 10:
                    # print(data)
                    if (data[0] == 'ma'):  # 表示基站0到基站x的距离
                        if (
                                data[1] != '0e'
                        ):  # MASK=e(0000 1111)表示 RANGE0,RANGE1,RANGE2,RANGE3 都有效
                            print("ma's Range 只有 " + data[1] + " 工作。")
                            # break
                        else:
                            # 16进制转为10进制，距离单位：mm
                            # range_0 = int(data[2],16) range_0没有'ma'对应的操作说明
                            # self.serial__receive_text.insertPlainText(unicode_data)
                            range_1 = int(data[3], 16)
                            range_2 = int(data[4], 16)
                            # range_3 = int(data[5],16)
                            # print("基站0到基站1的距离：%d"%(range_1)+"，基站0到基站2的距离：%d"%(range_2)+"，基站0到基站3的距离：%d"%(range_3))

                    else:  # data[0] == 'mc' or 'mr' ：表示标签x到基站y的距离
                        if (data[1] != '07'
                            ):  # MASK=7(0000 0111)表示 RANGE0,RANGE1,RANGE2 都有效
                            print("mc's Range 只有 " + data[1] + " 工作。")
                            # break
                        else:
                            # 16进制转为10进制，距离单位：mm
                            range_0 = int(data[2], 16)
                            range_1 = int(data[3], 16)
                            range_2 = int(data[4], 16)
                            # range_3 = int(data[5],16)
                            # print("标签x到基站0的距离：%d" % (range_0) +
                            #       "，标签x到基站1的距离：%d" % (range_1) +
                            #       "，标签x到基站2的距离：%d" % (range_2))

                            anchor_0 = np.array([0, 0], dtype=np.int64)
                            anchor_1 = np.array([7500, 0], dtype=np.int64)
                            anchor_2 = np.array([0, 5000], dtype=np.int64)
                            tag_position = self.getLocation(
                                anchor_0, anchor_1, anchor_2, range_0, range_1, range_2)
                            # if (tag_position[0]-anchor_2[0])**2 + (tag_position[1]-anchor_2[1])**2 > range_2:

                            if tag_position[1] != -1:
                                # print("标签坐标X:%f" %
                                #       tag_position[0] + "，Y:%f" % tag_position[1])
                                self.graphics([tag_position[0],tag_position[1]])

                                self.serial_signal.connect(
                                    otherClass.robot_position)
                                self.serial_signal.emit(
                                    tag_position[0], tag_position[1])

        else:
            pass

    def getLocation(self, anchor_0, anchor_1, anchor_2, range_0, range_1, range_2):
        """ 根据trilateration 计算标签的坐标 """
        tag_position = np.array([0, 0], dtype=np.int64)
        tag_position[0] = int(
            (range_0**2 - range_1**2 + anchor_1[0]**2) / (2 * anchor_1[0]))
        distance = range_0**2 - tag_position[0]**2
        # print(type(distance))
        if distance > 0:
            tag_position[1] = np.sqrt(distance)
        else:
            tag_position[1] = -1

        return tag_position

        # ValueError: cannot convert float NaN to integer #17

    def graphics(self,newPos = [0,0]):
        """ qt绘图 """
        axis_x = 750
        axis_y = 500
        
        # self.rect = QRectF(0,0,w-10,h-10)
        # self.scene = QGraphicsScene(self.rect)
        self.scene = QGraphicsScene()

        self.graphicsView.setScene(self.scene)
        
        
        self.scene.addRect(0,0,axis_x,axis_y)

        self.scene.addEllipse(0,0,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(0,axis_y,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(axis_x,0,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))
        self.scene.addEllipse(axis_x,axis_y,10,10, brush = QBrush(QColor.fromRgb(120, 50, 255)))

        self.scene.addLine(0,0,axis_x,0, pen = QPen(QColor.fromRgb(255, 0, 0)))
        self.scene.addLine(0,0,0,axis_y, pen = QPen(QColor.fromRgb(255, 0, 0)))


        self.anchor_0 = np.array([0, 0], dtype=np.int64)
        self.anchor_1 = np.array([axis_x, 0], dtype=np.int64)
        self.anchor_2 = np.array([0, axis_y], dtype=np.int64)

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
                

        robot_item = QGraphicsEllipseItem(newPos[0]/10, newPos[1]/10, 15, 15)
        robot_item.setBrush(QBrush(QColor.fromRgb(0, 255, 255)))
        self.scene.addItem(robot_item)

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


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.newDot = [0, 0]
        self.dot, = self.axes.plot([], [], 'ro')

        # self.gen_dot()
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, frames=self.gen_dot, interval=500, repeat=True)

    def compute_initial_figure(self):
        """ 绘制铺砖图纸 """
        plt.xlabel("axis_X", fontsize=10)
        plt.ylabel("axis_Y", fontsize=10)
        plt.xlim(0, 7500)
        plt.ylim(0, 5000)
        global currentAxis
        currentAxis = plt.gca()  # gca(): Get the current Axes
        currentAxis.set_aspect('equal', adjustable='box')  # x,y 相同的分度尺

        self.anchor_0 = np.array([0, 0], dtype=np.int64)
        self.anchor_1 = np.array([7500, 0], dtype=np.int64)
        self.anchor_2 = np.array([0, 5000], dtype=np.int64)

        self.axis_x_point = [self.anchor_0[0],
                             self.anchor_1[0], self.anchor_2[0]]
        self.axis_y_point = [self.anchor_0[1],
                             self.anchor_1[1], self.anchor_2[1]]
        self.axes.scatter(self.axis_x_point, self.axis_y_point, s=100, c='blue',
                          clip_on=False)  # clip_on = False：不裁剪原点

        # plt.plot(anchor_0[0],anchor_0[1],anchor_1[0],anchor_1[1],c = "red",linewidth = 3)
        self.axes.plot([self.anchor_0[0], self.anchor_1[0]],
                       [self.anchor_0[1], self.anchor_1[1]], c="purple", linewidth=4)  # 在两点之间作出一条直线
        self.axes.plot([self.anchor_0[0], self.anchor_2[0]], [
            self.anchor_0[1], self.anchor_2[1]], c="purple", linewidth=4)

        global brick_width, brick_height
        brick_width = 1000  # 砖长：300mm
        brick_height = 1000
        self.brick_gap = 50  # 砖间隙：5mm

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

                self.rectangle = patches.Rectangle((self.brick_x, self.brick_y), brick_width, brick_height, linewidth=1,
                                                   edgecolor='r', facecolor='none')
                # Add the patch to the Axes
                currentAxis.add_patch(self.rectangle)

        
    def gen_dot(self):
        print("position: (%d" % robot_point[0]+"，%d" % robot_point[1]+")")

        # 根据robot的位置，绘制相应砖的全色
        # self.compute_initial_figure()
        # for k in range(height_num * width_num):
        #     if robot_point[0] >= bricks[k][2] and robot_point[0] <= bricks[k][2] + brick_width and robot_point[1] >= bricks[k][3] and robot_point[1] <= bricks[k][3] + brick_height:
        #         bricks[k][4] = 1
        #         self.fillRectangle = plt.Rectangle(
        #             (bricks[k][2], bricks[k][3]), brick_width, brick_height, linewidth=1, facecolor='y')
        #         currentAxis.add_patch(self.fillRectangle)
        #     else:
        #         bricks[k][4] = 0

       
        # for brick in bricks:  # 铺完一块砖就覆盖颜色
        #     if brick[4] == 1:
        #         self.fillRectangle = plt.Rectangle(
        #             (brick[2], brick[3]), brick_width, brick_height, linewidth=1, facecolor='y')
        #     else:
        #         self.fillRectangle = plt.Rectangle(
        #             (brick[2], brick[3]), brick_width, brick_height, linewidth=1, facecolor='none')
        #     currentAxis.add_patch(self.fillRectangle)


        self.newDot = [robot_point[0], robot_point[1]]
        yield self.newDot

    def animate(self, newDot):
        self.dot.set_data(newDot[0], newDot[1])
        return self.dot,

    @pyqtSlot(int, int)
    def robot_position(self, x, y):
        # print("Robot's position: (%d" % x+"，%d" % y+")")
        global robot_point
        robot_point = [x, y]
        self.gen_dot()


class ApplicationWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=8, height=8, dpi=100)
        l.addWidget(dc)

        # self.main_widget.setFocus()


if __name__ == '__main__':
    serial_app = QtWidgets.QApplication(sys.argv)
   
    plot_form = ApplicationWindow()
    plot_form.resize(800, 800)
    plot_form.show()

    serial_form = Pyqt5_Serial()
    serial_form.show()

    sys.exit(serial_app.exec_())
