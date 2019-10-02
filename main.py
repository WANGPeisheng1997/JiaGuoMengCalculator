import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import *
import os

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, config=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self, config=config)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    if os.path.exists("config.json"):
        file = open('config.json', 'r')
        config = json.load(file)
        file.close()
        myWin = MyWindow(config=config)
    else:
        myWin = MyWindow()

    myWin.show()
    sys.exit(app.exec_())