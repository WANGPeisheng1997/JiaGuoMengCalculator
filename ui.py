from PyQt5 import QtCore, QtGui, QtWidgets
import json
from algorithm import Calculator
import os
from config import Config
from static import residence_buildings, commerce_buildings, industry_buildings, default_blacklist, modes
from update import get_latest_version


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

        self.blackListLabel = QtWidgets.QLabel(self)
        self.blackListLabel.setGeometry(QtCore.QRect(280, 20, 40, 16))
        self.blackListLabel.setText("黑名单")
        self.blackListLabel.setAlignment(QtCore.Qt.AlignCenter)

    def add_building(self, name, config):
        if config is None:
            star_default = 5
            level_default = 800
            buff_default = 0
            blacklist = default_blacklist
        else:
            default_value = config.buildings_config[name]
            star_default = default_value["star"]
            level_default = default_value["level"]
            buff_default = default_value["buff"]
            blacklist = config.blacklist_config

        y = len(self.buildings_label) * 25 + 45

        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(10, y, 70, 16))
        label.setText(name)

        # starLineEdit = QtWidgets.QLineEdit(self)
        # starLineEdit.setGeometry(QtCore.QRect(80, y, 40, 20))
        # starLineEdit.setText(str(star_default))

        starSpinBox = QtWidgets.QSpinBox(self)
        starSpinBox.setMaximum(5)
        starSpinBox.setMinimum(1)
        starSpinBox.setGeometry(QtCore.QRect(80, y, 40, 20))
        starSpinBox.setValue(star_default)

        levelLineEdit = QtWidgets.QLineEdit(self)
        levelLineEdit.setGeometry(QtCore.QRect(130, y, 40, 20))
        levelLineEdit.setText(str(level_default))

        buffLineEdit = QtWidgets.QLineEdit(self)
        buffLineEdit.setGeometry(QtCore.QRect(190, y, 70, 20))
        buffLineEdit.setText(str(buff_default))

        blackListCheckBox = QtWidgets.QCheckBox(self)
        blackListCheckBox.setGeometry(QtCore.QRect(290, y, 20, 20))
        blackListCheckBox.setObjectName(name + "black")
        if name in blacklist:
            blackListCheckBox.setChecked(True)

        self.buildings_label.append(label)
        self.buildings_star.append(starSpinBox)
        self.buildings_level.append(levelLineEdit)
        self.buildings_buff.append(buffLineEdit)

    def get_buildings_info(self):
        buildings_info = {}
        for count in range(len(self.buildings_label)):
            name = self.buildings_label[count].text()
            star = self.buildings_star[count].value()
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

    def add_buff(self, name, big_type, small_type, config):
        if config is None:
            buff_default = 0
        else:
            buff_default = config.buffs_config[big_type][small_type]

        y = len(self.buff) * 25 + 25

        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(10, y, 160, 16))
        label.setText(name)

        buffLineEdit = QtWidgets.QLineEdit(self)
        buffLineEdit.setGeometry(QtCore.QRect(190, y, 70, 20))
        buffLineEdit.setText(str(buff_default))

        self.buff.append(buffLineEdit)

    def get_buffs_info(self):
        buffs_info = {}
        for count in range(len(self.buff_types)):
            type = self.buff_types[count]
            value = self.buff[count].text()
            buffs_info[type] = int(value)
        return buffs_info


class Ui_MainWindow(object):
    def __init__(self):
        self.config = None
        if os.path.exists("config.json"):
            file = open('config.json', 'r')
            json_config = json.load(file)
            file.close()
            self.config = Config()
            self.config.init_config_from_json(json_config)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1330, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.residenceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(10, 20, 330, 300), "residence", "住宅建筑")
        for building in residence_buildings:
            self.residenceGroupBox.add_building(building, self.config)

        self.commerceGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(350, 20, 330, 300), "commerce", "商业建筑")
        for building in commerce_buildings:
            self.commerceGroupBox.add_building(building, self.config)

        self.industryGroupBox = BuildingGroupBox(self.centralwidget, QtCore.QRect(690, 20, 330, 300), "industry", "工业建筑")
        for building in industry_buildings:
            self.industryGroupBox.add_building(building, self.config)

        self.policyGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(10, 340, 270, 180), "policy", "政策加成")
        self.policyGroupBox.buff_labels.append("家国之光与国庆的收入增加(%)")
        self.policyGroupBox.buff_types.append("jiaguozhiguang")
        for count in range(len(self.policyGroupBox.buff_labels)):
            self.policyGroupBox.add_buff(name=self.policyGroupBox.buff_labels[count], big_type="policy", small_type=self.policyGroupBox.buff_types[count], config=self.config)

        self.albumGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(290, 340, 270, 160), "album", "相册加成")
        for count in range(len(self.albumGroupBox.buff_labels)):
            self.albumGroupBox.add_buff(name=self.albumGroupBox.buff_labels[count], big_type="album", small_type=self.albumGroupBox.buff_types[count], config=self.config)

        self.missionGroupBox = BuffGroupBox(self.centralwidget, QtCore.QRect(570, 340, 270, 160), "mission", "城市任务加成")
        for count in range(len(self.missionGroupBox.buff_labels)):
            self.missionGroupBox.add_buff(name=self.missionGroupBox.buff_labels[count], big_type="mission", small_type=self.missionGroupBox.buff_types[count], config=self.config)

        self.othersGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.othersGroupBox.setGeometry(QtCore.QRect(850, 340, 170, 160))
        self.othersGroupBox.setTitle("其他选项")

        self.modeLabel = QtWidgets.QLabel(self.othersGroupBox)
        self.modeLabel.setGeometry(QtCore.QRect(20, 20, 60, 20))
        self.modeLabel.setText("模式")

        self.modeComboBox = QtWidgets.QComboBox(self.othersGroupBox)
        self.modeComboBox.setGeometry(QtCore.QRect(90, 20, 60, 20))
        self.modeComboBox.addItems(["在线", "离线", "火车"])
        self.modeComboBox.setEnabled(False)

        self.goldLabel = QtWidgets.QLabel(self.othersGroupBox)
        self.goldLabel.setGeometry(QtCore.QRect(20, 45, 60, 20))
        self.goldLabel.setText("拥有金币")

        self.goldLineEdit = QtWidgets.QLineEdit(self.othersGroupBox)
        self.goldLineEdit.setGeometry(QtCore.QRect(90, 45, 60, 20))
        if self.config is None:
            self.goldLineEdit.setText("8.88aa")
        else:
            self.goldLineEdit.setText(self.config.gold_config)


        self.helpLabel = QtWidgets.QLabel(self.othersGroupBox)
        self.helpLabel.setGeometry(QtCore.QRect(20, 70, 140, 20))
        self.helpLabel.setText("(金币直接按游戏内格式)")

        self.resultGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.resultGroupBox.setGeometry(QtCore.QRect(1030, 20, 280, 480))
        self.resultGroupBox.setTitle("计算结果")

        self.resultLabel = QtWidgets.QLabel(self.resultGroupBox)
        self.resultLabel.setGeometry(QtCore.QRect(20, 20, 250, 500))
        self.resultLabel.setText("")
        self.resultLabel.setAlignment(QtCore.Qt.AlignTop)

        self.lastestVersionLabel = QtWidgets.QLabel(self.centralwidget)
        self.lastestVersionLabel.setGeometry(QtCore.QRect(20, 530, 250, 20))
        self.lastestVersionLabel.setText(get_latest_version())

        self.currentVersionLabel = QtWidgets.QLabel(self.centralwidget)
        self.currentVersionLabel.setGeometry(QtCore.QRect(20, 550, 250, 20))
        self.currentVersionLabel.setText("当前本地版本：V2.1")

        self.openUrlLabel = QtWidgets.QLabel(self.centralwidget)
        self.openUrlLabel.setGeometry(QtCore.QRect(20, 580, 270, 20))
        self.openUrlLabel.setText('<a href="https://github.com/WANGPeisheng1997/JiaGuoMengCalculator" style="color:#0000ff;">下载最新版本</a>')
        self.openUrlLabel.setOpenExternalLinks(True)

        # self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        # self.saveButton.setGeometry(QtCore.QRect(440, 540, 100, 23))
        # self.saveButton.setObjectName("saveButton")
        # self.saveButton.setText("保存配置文件")
        # self.saveButton.clicked.connect(self.save_info)

        self.calculateButton = QtWidgets.QPushButton(self.centralwidget)
        self.calculateButton.setGeometry(QtCore.QRect(1100, 520, 140, 23))
        self.calculateButton.setObjectName("calculateButton")
        self.calculateButton.setText("仅计算当前最优排布")
        self.calculateButton.clicked.connect(self.calculate)

        self.calculateUpgradeButton = QtWidgets.QPushButton(self.centralwidget)
        self.calculateUpgradeButton.setGeometry(QtCore.QRect(1100, 550, 140, 23))
        self.calculateUpgradeButton.setObjectName("calculateUpgradeButton")
        self.calculateUpgradeButton.setText("计算升级后最优排布")
        self.calculateUpgradeButton.clicked.connect(self.calculate_upgrade)

        self.progressLabel = QtWidgets.QLabel(self.centralwidget)
        self.progressLabel.setGeometry(QtCore.QRect(540, 520, 250, 20))
        self.progressLabel.setText("计算时间可能较长，请勿关闭窗口！")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(500, 550, 300, 23))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "家国梦建筑最优化计算器 V2.1"))

    def save_info(self, only_current = False):
        residence_buildings_info = self.residenceGroupBox.get_buildings_info()
        commerce_buildings_info = self.commerceGroupBox.get_buildings_info()
        industry_buildings_info = self.industryGroupBox.get_buildings_info()
        all_buildings_info = {**residence_buildings_info, **commerce_buildings_info, **industry_buildings_info}
        policy_buffs_info = self.policyGroupBox.get_buffs_info()
        album_buffs_info = self.albumGroupBox.get_buffs_info()
        mission_buffs_info = self.missionGroupBox.get_buffs_info()
        all_buffs_info = {"policy": policy_buffs_info, "album": album_buffs_info, "mission": mission_buffs_info}

        blacklist = []
        for building in commerce_buildings + residence_buildings + industry_buildings:
            child = self.centralwidget.findChild(QtWidgets.QCheckBox, building + "black")
            if child.isChecked():
                blacklist.append(building)

        whitelist = []
        mode = modes[self.modeComboBox.currentIndex()]
        gold = self.goldLineEdit.text()

        all_info = {"buildings": all_buildings_info, "buffs": all_buffs_info, "blacklist": blacklist, "whitelist": whitelist, "mode": mode, "gold": gold, "only_current": only_current}
        js = json.dumps(all_info, indent=4, separators=(',', ': '))
        file = open('config.json', 'w')
        file.write(js)
        file.close()

    def calculate(self):
        self.save_info(only_current=True)
        file = open('config.json', 'r')
        json_config = json.load(file)
        file.close()
        config = Config()
        config.init_config_from_json(json_config)
        calculator = Calculator(config)
        calculator.calculate(progress_bar=self.progressBar)
        resultFile = open("result.txt", 'r')
        self.resultLabel.setText(resultFile.read())
        resultFile.close()

    def calculate_upgrade(self):
        self.save_info()
        file = open('config.json', 'r')
        json_config = json.load(file)
        file.close()
        config = Config()
        config.init_config_from_json(json_config)
        calculator = Calculator(config)
        calculator.calculate(progress_bar=self.progressBar)
        resultFile = open("result.txt", 'r')
        self.resultLabel.setText(resultFile.read())
        resultFile.close()
