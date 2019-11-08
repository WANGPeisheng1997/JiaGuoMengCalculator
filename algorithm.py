import numpy as np
from tqdm import tqdm
from queue import PriorityQueue as PQ
import pandas as pd
from itertools import combinations, product
from concurrent.futures import ProcessPoolExecutor
import static
import copy

def comb(a, b):
    return a * (a-1) * (a-2) / 6

class NamedPQ(object):
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name
        return

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority


class Calculator:
   
    # set as the cpu core number 
    MAX_WORKER_NUMBER = 8
    
    def __init__(self, config):
        self.config = config
        self.buildings_config = config.buildings_config
        self.buffs_config = config.buffs_config
        self.policy_buff = self.buffs_config["policy"]
        self.album_buff = self.buffs_config["album"]
        self.mission_buff = self.buffs_config["mission"]
        self.blacklist = config.blacklist_config
        self.only_current = config.only_current

        self.buildStars = {1: [], 2: [], 3: [], 4: [], 5: []}
        for build in self.buildings_config:
            star = self.buildings_config[build]["star"]
            self.buildStars[star].append(build)

        self.mode = 'online'
        self.totalGold = config.gold_config

    def showLetterNum(self, num):
        index = list(static.UnitDict.keys())[int(np.log10(num))//3]
        return str(np.round(num/static.UnitDict[index], 2)) + index

    def calculateComb(self, buildings, MaxIncome=0, output=False):
        NowEffect = 1e300
        NeededEffect = 0
        Golds = self.totalGold
        buildtuple = buildings[0] + buildings[1] + buildings[2]
        NowGrade = [self.buildings_config[build]["level"] for build in buildtuple]
        Rarities = [self.buildsDict[build]['rarity'] for build in buildtuple]
        comboBuff = dict()
        for build in buildtuple:
            comboBuff[build] = 1
        for build in buildtuple:
            for buffedBuild, buffMultiple in self.buildsDict[build]['buff'].items():
                if buffedBuild in buildtuple:
                    comboBuff[buffedBuild] += buffMultiple
                elif buffedBuild == 'industry':
                    comboBuff[buildtuple[0]] += buffMultiple
                    comboBuff[buildtuple[1]] += buffMultiple
                    comboBuff[buildtuple[2]] += buffMultiple
                elif buffedBuild == 'commerce':
                    comboBuff[buildtuple[3]] += buffMultiple
                    comboBuff[buildtuple[4]] += buffMultiple
                    comboBuff[buildtuple[5]] += buffMultiple
                elif buffedBuild == 'residence':
                    comboBuff[buildtuple[6]] += buffMultiple
                    comboBuff[buildtuple[7]] += buffMultiple
                    comboBuff[buildtuple[8]] += buffMultiple

        basemultiples = [self.buildsDict[build]['baseIncome'] * comboBuff[build] \
                         for i, build in enumerate(buildtuple)]
        IncomeUnupgrade = sum([basemultiples[i] * \
                               self.Upgrade['incomePerSec'][NowGrade[i] - 1] \
                               for i, build in enumerate(buildtuple)])
        Income = IncomeUnupgrade

        if not self.only_current:
            upgradePQ = PQ()
            for i, build in enumerate(buildtuple):
                upgradePQ.put(NamedPQ(-self.Upgrade['Ratio' + Rarities[i]][NowGrade[i] - 1] * basemultiples[i],
                                      i))

            while Golds > 0 and NowEffect > NeededEffect:
                i = upgradePQ.get().name
                NowGradeI = NowGrade[i]
                if NowGradeI < 2000:
                    Golds -= self.Upgrade[Rarities[i]][NowGrade[i] + 1]
                    NowGrade[i] += 1  # upgrade build
                    upgradePQ.put(NamedPQ(-self.Upgrade['Ratio' + Rarities[i]][NowGrade[i] - 1] * basemultiples[i],
                                          i))
                    Income += self.Upgrade['incomeIncrease'][NowGrade[i]] * basemultiples[i]
                    if self.totalGold - Golds==0:
                        NowEffect = 0
                    else:
                        NowEffect = (Income - IncomeUnupgrade) / (self.totalGold - Golds)
                    NeededEffect = (MaxIncome - Income) / Golds
                elif upgradePQ.empty():
                    break

        if output:
            resultFile = open("result.txt", 'w', encoding='utf-8')
            print('消耗完金币后的最优策略：', file=resultFile)
            print('工业建筑：%s、%s、%s' % (buildings[0]), file=resultFile)
            print('商业建筑：%s、%s、%s' % (buildings[1]), file=resultFile)
            print('住宅建筑：%s、%s、%s' % (buildings[2]), file=resultFile)

            print(file=resultFile)
            print('总秒收入：', self.showLetterNum(Income), file=resultFile)
            print(file=resultFile)

            print('升级后各建筑等级(括号内为提升量)：', file=resultFile)
            for i, build in enumerate(buildtuple):
                print('{:<8}\t'.format(build), '%d(+%d)' % (NowGrade[i], NowGrade[i] - self.buildings_config[build]["level"]), file=resultFile)
            print(file=resultFile)

            multiples = [basemultiples[i] * self.Upgrade['incomePerSec'][NowGrade[i] - 1] \
                         for i, build in enumerate(buildtuple)]
            print('升级后各建筑秒收入：', file=resultFile)
            for i, x in enumerate(multiples):
                print('{:<8}\t'.format(buildtuple[i]), self.showLetterNum(x), file=resultFile)
            print(file=resultFile)

            # if not upgradePQ.empty():
            #     ToUpgrade = upgradePQ.get()
            #     print('优先升级:', buildtuple[ToUpgrade.name], file=resultFile)
            #     print('每金币收益:', -ToUpgrade.priority, file=resultFile)

            resultFile.close()
        else:
            return Income, (buildings, NowGrade), NowEffect

    def calculate(self, progress_bar = None):

        if self.totalGold == "0":
            self.totalGold = 0
        else:
            # find unit
            success = False
            for unit in static.UnitDict:
                pos = self.totalGold.find(unit)
                if pos != -1:
                    # this is the unit
                    GoldNum, Unit = self.totalGold[:pos], self.totalGold[pos:]
                    self.totalGold = float(GoldNum) * static.UnitDict[Unit]
                    success = True
                    break
            if not success:
                print('单位错误,请检查金币输入')
                return

        if self.mode == 'online':
            Industrial = copy.deepcopy(static.industry_buildings)
            Business = copy.deepcopy(static.commerce_buildings)
            Residence = copy.deepcopy(static.residence_buildings)
            for build in self.blacklist:
                if build in Industrial:
                    Industrial.remove(build)
                if build in Business:
                    Business.remove(build)
                if build in Residence:
                    Residence.remove(build)
            totalBuilds = Business + Residence + Industrial

        BaseIncome = pd.read_csv('data/baseIncome.csv', encoding='gb2312')
        self._Upgrade = pd.read_csv('data/upgrade.csv')
        self.Upgrade = self._Upgrade.to_dict()

        searchSpace = product(combinations(Industrial, 3),
                              combinations(Business, 3), combinations(Residence, 3))
        searchSpaceSize = comb(len(Industrial), 3) * comb(len(Business), 3) * comb(len(Residence), 3)

        self.buildsDict = dict()

        for star, builds in self.buildStars.items():
            for build in builds:
                if build in totalBuilds:
                    incomeRow = BaseIncome[(BaseIncome.buildName == build) & (BaseIncome.star == star)]
                    self.buildsDict[build] = {
                        'category': incomeRow.category.values[0],
                        'star': star,
                        'rarity': incomeRow.rarity.values[0],
                        'baseIncome': incomeRow.baseIncome.values[0],
                        'buff': dict()
                    }

        for build, info in self.buildsDict.items():
            self.buildsDict[build]['baseIncome'] *= \
                (1 + self.policy_buff['global']/100 + self.policy_buff['online']/100 + self.policy_buff[info['category']]/100 + self.policy_buff['jiaguozhiguang']/100) * \
                (1 + self.album_buff['global']/100 + self.album_buff['online']/100 + self.album_buff[info['category']]/100) * \
                (1 + self.buildings_config[build]['buff']/100 + self.mission_buff['global']/100 + self.mission_buff['online']/100 + self.mission_buff[info['category']]/100)

        for build, info in self.buildsDict.items():
            if build in static.buffs_100:
                for buffedBuild in static.buffs_100[build]:
                    self.buildsDict[build]['buff'][buffedBuild] = info['star']
            if build in static.buffs_50:
                for buffedBuild in static.buffs_50[build]:
                    self.buildsDict[build]['buff'][buffedBuild] = info['star'] * 0.5

            if build in static.buffs_ind:
                self.buildsDict[build]['buff']['industry'] = static.buffs_ind[build][info['star'] - 1]
            if build in static.buffs_bus:
                self.buildsDict[build]['buff']['commerce'] = static.buffs_bus[build][info['star'] - 1]
            if build in static.buffs_res:
                self.buildsDict[build]['buff']['residence'] = static.buffs_res[build][info['star'] - 1]

        results = PQ()

        MaxIncome = 0
        MaxStat = 0

        if progress_bar is not None:
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(self.MAX_WORKER_NUMBER * 2)
            progress_bar.setValue(0)

        with ProcessPoolExecutor(max_workers=self.MAX_WORKER_NUMBER) as ex:
            total = int(searchSpaceSize)
            step = total // (self.MAX_WORKER_NUMBER * 2) 
            futures = [ex.submit(self.workerWrapper, searchSpace, i, i + step) for i in range(0, total, step)]
            for f in tqdm(futures, total=len(futures),
                              bar_format='{percentage:3.0f}%,{elapsed}<{remaining}|{bar}|{n_fmt}/{total_fmt},{rate_fmt}{postfix}'):
                TotalIncome, Stat, NowEffect = f.result()
                if TotalIncome > MaxIncome:
                    MaxIncome = TotalIncome
                    MaxStat = Stat
                    MaxEffect = NowEffect
                if progress_bar is not None:
                    progress_bar.setValue(progress_bar.value()+1)

        self.calculateComb(MaxStat[0], output=True)

    def workerWrapper(self, searchSpace, start, end):
        _MaxIncome = 0
        _MaxStat = 0
        for ind, buildings in enumerate(searchSpace):
            if start > ind:
                continue
            if end <= ind:
                break
            TotalIncome, Stat, NowEffect = self.calculateComb(buildings, _MaxIncome)
            if TotalIncome > _MaxIncome:
                _MaxIncome = TotalIncome
                _MaxStat = Stat
                _MaxEffect = NowEffect
        return _MaxIncome, _MaxStat, _MaxEffect
