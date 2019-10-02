from PyQt5 import QtCore, QtGui, QtWidgets
import json
from algorithm import Calculator
import os

commerce_buildings = '便利店 五金店 服装店 菜市场 学校 图书城 商贸中心 加油站 民食斋 媒体之声'.split()
residence_buildings = '木屋 居民楼 钢结构房 平房 小型公寓 人才公寓 花园洋房 中式小楼 空中别墅 复兴公馆'.split()
industry_buildings = '木材厂 食品厂 造纸厂 水厂 电厂 钢铁厂 纺织厂 零件厂 企鹅机械 人民石油'.split()

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
        self.buffLabel.setGeometry(QtCore.QRect(180, 20, 90, 16))
        self.buffLabel.setText("城市任务加成(%)")
        self.buffLabel.setAlignment(QtCore.Qt.AlignCenter)


    def add_building(self, name, star_default = 5, level_default = 800, buff_default = 0):
        y = len(self.buildings_label) * 25 + 45

        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(10, y, 70, 16))
        label.setText(name)

        starLineEdit = QtWidgets.QLineEdit(self)
        starLineEdit.setGeometry(QtCore.QRect(80, y, 40, 20))
        starLineEdit.setText(str(star_default))

        levelLineEdit = QtWidgets.QLineEdit(self)
        levelLineEdit.setGeometry(QtCore.QRect(130, y, 40, 20))
        levelLineEdit.setText(str(level_default))

        buffLineEdit = QtWidgets.QLineEdit(self)
        buffLineEdit.setGeometry(QtCore.QRect(190, y, 70, 20))
        buffLineEdit.setText(str(buff_default))

        self.buildings_label.append(label)
        self.buildings_star.append(starLineEdit)
        self.buildings_level.append(levelLineEdit)
        self.buildings_buff.append(buffLineEdit)

    def get_buildings_info(self):
        buildings_info = {}
        for count in range(len(self.buildings_label)):
            name = self.buildings_label[count].text()
            star = self.buildings_star[count].text()
            level = self.buildings_level[count].text()
            buff = self.buildings_buff[count].text()
            buildings_info[name] = {"star": int(star), "level": int(level), "buff": int(buff)}
        return buildings_info


class BuffGroupBox(QtWidgets.QGroupBox):
    def __init__(self, widget, rect, name, title):
        super().__init__(widget)
        self.setGeometry(rect)
        self.setObjectName(name)
        self.setTitle(title)

        self.buff = []
        self.buff_labels = ["所有建筑的收入增加(%)", "在线时所有建筑的收入增加(%)", "住宅建筑的收入增加(%)", "商业建筑的收入增加(%)", "工业建筑的收入增加(%)"]
        self.buff_types = ["global", "online", "residence", "commerce", "industry"]

        for label in self.buff_labels:
            self.add_buff(label)

    def add_buff(self, name):
        y = len(self.buff) * 25 + 25

        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(10, y, 160, 16))
        label.setText(name)

        buffLineEdit = QtWidgets.QLineEdit(self)
        buffLineEdit.setGeometry(QtCore.QRect(190, y, 70, 20))
        buffLineEdit.setText("0")

        self.buff.append(buffLineEdit)

    def get_buffs_info(self):
        buffs_info = {}
        for count in range(len(self.buff_types)):
            type = self.buff_types[count]
            value = self.buff[count].text()
            buffs_info[type] = int(value)
        return buffs_info


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, config=None):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.config = config

        if config is not None:
            self.load_config()

        self.residenceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(10, 20, 280, 300), "residence", "住宅建筑")
        for building in residence_buildings:
            if config is None:
                self.residenceGroupBox.add_building(building)
            else:
                default_value = self.buildings_config[building]
                self.residenceGroupBox.add_building(building, star_default=default_value["star"], level_default=default_value["level"], buff_default=default_value["buff"])

        self.commerceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(300, 20, 280, 300), "commerce", "商业建筑")
        for building in commerce_buildings:
            if config is None:
                self.commerceGroupBox.add_building(building)
            else:
                default_value = self.buildings_config[building]
                self.commerceGroupBox.add_building(building, star_default=default_value["star"], level_default=default_value["level"], buff_default=default_value["buff"])

        self.industryGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(590, 20, 280, 300), "industry", "工业建筑")
        for building in industry_buildings:
            if config is None:
                self.industryGroupBox.add_building(building)
            else:
                default_value = self.buildings_config[building]
                self.industryGroupBox.add_building(building, star_default=default_value["star"], level_default=default_value["level"], buff_default=default_value["buff"])

        self.policyGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(10, 340, 280, 180), "policy", "政策加成")
        self.policyGroupBox.add_buff("家国之光的收入增加(%)")
        self.policyGroupBox.buff_labels.append("家国之光的收入增加(%)")
        self.policyGroupBox.buff_types.append("jiaguozhiguang")
        if config is not None:
            for count in range(len(self.policyGroupBox.buff)):
                buff_dict = self.buffs_config['policy']
                buff_type = self.policyGroupBox.buff_types[count]
                self.policyGroupBox.buff[count].setText(str(buff_dict[buff_type]))

        self.albumGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(300, 340, 280, 160), "album", "相册加成")
        if config is not None:
            for count in range(len(self.albumGroupBox.buff)):
                buff_dict = self.buffs_config['album']
                buff_type = self.albumGroupBox.buff_types[count]
                self.albumGroupBox.buff[count].setText(str(buff_dict[buff_type]))

        self.missionGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(590, 340, 280, 160), "mission", "城市任务加成")
        if config is not None:
            for count in range(len(self.missionGroupBox.buff)):
                buff_dict = self.buffs_config['mission']
                buff_type = self.missionGroupBox.buff_types[count]
                self.missionGroupBox.buff[count].setText(str(buff_dict[buff_type]))

        self.resultGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.resultGroupBox.setGeometry(QtCore.QRect(880, 20, 280, 480))
        self.resultGroupBox.setTitle("计算结果")

        self.resultLabel = QtWidgets.QLabel(self.resultGroupBox)
        self.resultLabel.setGeometry(QtCore.QRect(20, 20, 250, 500))
        self.resultLabel.setText("")
        self.resultLabel.setAlignment(QtCore.Qt.AlignTop)


        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(400, 540, 100, 23))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("保存建筑信息")
        self.saveButton.clicked.connect(self.save_info)

        self.calculateButton = QtWidgets.QPushButton(self.centralwidget)
        self.calculateButton.setGeometry(QtCore.QRect(970, 540, 100, 23))
        self.calculateButton.setObjectName("calculateButton")
        self.calculateButton.setText("计算最优排布")
        self.calculateButton.clicked.connect(self.calculate)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "家国梦建筑最优化计算器"))

    def save_info(self):
        residence_buildings_info = self.residenceGroupBox.get_buildings_info()
        commerce_buildings_info = self.commerceGroupBox.get_buildings_info()
        industry_buildings_info = self.industryGroupBox.get_buildings_info()
        all_buildings_info = {**residence_buildings_info, **commerce_buildings_info, **industry_buildings_info}
        policy_buffs_info = self.policyGroupBox.get_buffs_info()
        album_buffs_info = self.albumGroupBox.get_buffs_info()
        mission_buffs_info = self.missionGroupBox.get_buffs_info()
        all_buffs_info = {"policy": policy_buffs_info, "album": album_buffs_info, "mission": mission_buffs_info}
        all_info = {"buildings": all_buildings_info, "buffs": all_buffs_info}
        js = json.dumps(all_info, indent=4, separators=(',', ': '))
        file = open('config.json', 'w')
        file.write(js)
        file.close()

    def load_config(self):
        self.buildings_config = self.config["buildings"]
        self.buffs_config = self.config["buffs"]

    def calculate(self):
        self.save_info()
        if os.path.exists("config.json"):
            file = open('config.json', 'r')
            config = json.load(file)
            file.close()
        calculator = Calculator(config)
        calculator.calculate()
        resultFile = open("result.txt", 'r')
        self.resultLabel.setText(resultFile.read())
        resultFile.close()