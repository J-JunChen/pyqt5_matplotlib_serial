from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Worker(QObject):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)

    @pyqtSlot(str, str, int)
    def onJob(self, strA, strB, int1):
        print(strA, strB, int1)


class MyApp(QWidget):
    signal = pyqtSignal(str, str, int)
    def __init__(self, parent= None):
        super(MyApp, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.btn = QPushButton("start", self)
        self.btn.clicked.connect(self.start)
        self.show()

    def start(self):
        otherClass = Worker()
        self.signal.connect(otherClass.onJob)
        self.signal.emit("foo", "baz", 10)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())