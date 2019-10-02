from PyQt5 import QtCore, QtGui, QtWidgets


class BuildingGroupBox(QtWidgets.QGroupBox):
    def __init__(self, widget, rect, name, title):
        super().__init__(widget)
        self.setGeometry(rect)
        self.setObjectName(name)
        self.setTitle(title)

    def add_building(self, name):


class BuffGroupBox(QtWidgets.QGroupBox):
    def __init__(self, widget, rect, name):
        super().__init__(widget)
        self.setGeometry(rect)
        self.setObjectName(name)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(903, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.residenceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(10, 20, 251, 191), "residence", "住宅建筑")
        self.commerceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(270, 20, 251, 191), "commerce", "商业建筑")
        self.industryGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(530, 20, 251, 191), "industry", "工业建筑")

        self.policyGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(10, 220, 251, 191), "policy")
        self.albumGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(270, 220, 251, 191), "album")
        self.missionGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(530, 220, 251, 191), "mission")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "家国梦建筑最优化计算器"))
        self.policyGroupBox.setTitle(_translate("MainWindow", "政策加成"))
        self.missionGroupBox.setTitle(_translate("MainWindow", "城市任务加成"))
        self.albumGroupBox.setTitle(_translate("MainWindow", "相片加成"))
