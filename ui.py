from PyQt5 import QtCore, QtGui, QtWidgets

commerce_buildings = '便利店 五金店 服装店 菜市场 学校 图书城 商贸中心 加油站 民食斋 媒体之声'.split()
residence_buildings = '木屋 居民楼 钢结构房 平房 小型公寓 人才公寓 花园洋房 中式小楼 空中别墅 复兴公馆'.split()
industry_buildings = '木材厂 食品厂 造纸厂 水厂 电厂 钢铁厂 纺织厂 零件厂 企鹅机械 人民石油'.split()

Policy = {
    'Global':  6,
    'Online':  2,
    'Offline': 0,
    'Residence': 3,
    'Commercial': 9,
    'Industry': 9,
    'JiaGuoZhiGuang': 0.9
}

Photos = {
    'Global':  1.4,
    'Online':  1.4,
    'Offline': 0.7,
    'Residence': 2.4,
    'Commercial': 3,
    'Industry': 2.1,
}


class BuildingGroupBox(QtWidgets.QGroupBox):
    def __init__(self, widget, rect, name, title):
        super().__init__(widget)
        self.setGeometry(rect)
        self.setObjectName(name)
        self.setTitle(title)
        self.buildings_label = []
        self.buildings_star = []
        self.buildings_level = []
        self.buildings_buff = []

        self.nameLabel = QtWidgets.QLabel(self)
        self.nameLabel.setGeometry(QtCore.QRect(10, 20, 60, 16))
        self.nameLabel.setText("建筑名称")

        self.starLabel = QtWidgets.QLabel(self)
        self.starLabel.setGeometry(QtCore.QRect(80, 20, 40, 16))
        self.starLabel.setText("星级")
        self.starLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.levelLabel = QtWidgets.QLabel(self)
        self.levelLabel.setGeometry(QtCore.QRect(130, 20, 40, 16))
        self.levelLabel.setText("等级")
        self.levelLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.buffLabel = QtWidgets.QLabel(self)
        self.buffLabel.setGeometry(QtCore.QRect(180, 20, 80, 16))
        self.buffLabel.setText("城市任务加成")
        self.buffLabel.setAlignment(QtCore.Qt.AlignCenter)


    def add_building(self, name):
        y = len(self.buildings_label) * 25 + 45

        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(10, y, 70, 16))
        label.setText(name)

        starLineEdit = QtWidgets.QLineEdit(self)
        starLineEdit.setGeometry(QtCore.QRect(80, y, 40, 20))
        starLineEdit.setObjectName(name + "star")

        levelLineEdit = QtWidgets.QLineEdit(self)
        levelLineEdit.setGeometry(QtCore.QRect(130, y, 40, 20))
        levelLineEdit.setObjectName(name + "level")

        buffLineEdit = QtWidgets.QLineEdit(self)
        buffLineEdit.setGeometry(QtCore.QRect(180, y, 80, 20))
        buffLineEdit.setObjectName(name + "buff")

        self.buildings_label.append(label)
        self.buildings_star.append(starLineEdit)
        self.buildings_level.append(levelLineEdit)
        self.buildings_buff.append(buffLineEdit)


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

        self.residenceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(10, 20, 270, 300), "residence", "住宅建筑")
        for building in residence_buildings:
            self.residenceGroupBox.add_building(building)

        self.commerceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(290, 20, 270, 300), "commerce", "商业建筑")
        for building in commerce_buildings:
            self.commerceGroupBox.add_building(building)

        self.industryGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(570, 20, 270, 300), "industry", "工业建筑")
        for building in industry_buildings:
            self.industryGroupBox.add_building(building)

        self.policyGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(10, 350, 251, 191), "policy")
        self.albumGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(270, 350, 251, 191), "album")
        self.missionGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(530, 350, 251, 191), "mission")

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
