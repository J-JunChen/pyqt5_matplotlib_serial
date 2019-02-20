import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

dir_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前路径
sys.path.append(dir_path+'/view')

from Ui_serial import Ui_MainWindow


class Main_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle("俊杰很diao的UWB上位机")
    
    def drawLocation(self):
        
     

if __name__ == "__main__":
    main_app = QtWidgets.QApplication(sys.argv)
    main_form = Main_Window()
    main_form.show()
    sys.exit(main_app.exec_())