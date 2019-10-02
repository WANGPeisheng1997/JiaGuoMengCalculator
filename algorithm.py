import numpy as np
from tqdm import tqdm
from queue import PriorityQueue as PQ
import os
import pandas as pd
from scipy.special import comb
from itertools import combinations, product
from collections import defaultdict as ddict
import static

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

    def __init__(self, config):
        self.config = config
        self.buildings_config = self.config["buildings"]
        self.buffs_config = self.config["buffs"]
        self.policy_buff = self.buffs_config["policy"]
        self.album_buff = self.buffs_config["album"]
        self.mission_buff = self.buffs_config["mission"]

        self.buildStars = {1: [], 2: [], 3: [], 4: [], 5: []}
        for build in self.buildings_config:
            star = self.buildings_config[build]["star"]
            self.buildStars[star].append(build)

        self.mode = 'Online'  # 这个先不要改，后面计划增加供货模式和离线模式
        self.blacklist = {
            'Global': '',  # 在这里填写你没有或者完全不想用的建筑，空格分隔，优先级最高
            'Online': ''
        }
        self.totalGold = '1 aa'

    def calculateComb(self, buildings):
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

    #    upgradePQ = PQ()
    #    for i, build in enumerate(buildtuple):
    #        upgradePQ.put(NamedPQ(Upgrade['Ratio'+Rarities[i]].iloc[NowGrade[i]-1],
    #                              i))
    #    while Golds > 0:
    #        build = upgradePQ.get().name
    #        Golds -= Upgrade[Rarities[i]].iloc[NowGrade[i]+1]
    #        NowGrade[i] += 1 # upgrade build
    #        upgradePQ.put(NamedPQ(Upgrade['Ratio'+Rarities[i]].iloc[NowGrade[i]-1],
    #                              i))

        multiples = [self.buildsDict[build]['baseIncome'] * comboBuff[build] * \
                     self.Upgrade.incomePerSec.iloc[NowGrade[i]-1]\
                     for i, build in enumerate(buildtuple)]
        TotalIncome = sum(multiples)
        return (TotalIncome, (NowGrade, multiples))


    def showLetterNum(self, num):
        index = list(static.UnitDict.keys())[int(np.log10(num))//3]
        return str(np.round(num/static.UnitDict[index], 2)) + index


    def calculate(self):
        GoldNum, Unit = self.totalGold.split()
        try:
            self.totalGold = float(GoldNum) * static.UnitDict[Unit]
        except KeyError:
            print('单位错误,请检查金币输入')

        if self.mode == 'Online':
            Industrial = static.Industrial.split()
            Business = static.Business.split()
            Residence = static.Residence.split()
            for build in self.blacklist['Global'].split() + self.blacklist['Online'].split():
                if build in Industrial:
                    Industrial.remove(build)
                if build in Business:
                    Business.remove(build)
                if build in Residence:
                    Residence.remove(build)
            totalBuilds = Business + Residence + Industrial

        BaseIncome = pd.read_csv('baseIncome.csv', encoding='gb2312')
        self.Upgrade = pd.read_csv('upgrade.csv')

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
                (1 + self.policy_buff['global'] + self.policy_buff['online'] + self.policy_buff[info['category']] + self.policy_buff['jiaguozhiguang']) * \
                (1 + self.album_buff['global'] + self.album_buff['online'] + self.album_buff[info['category']]) * \
                (1 + self.buildings_config[build]['buff'] + self.mission_buff['global'] + self.mission_buff['online'] + self.mission_buff[info['category']])

        for build, info in self.buildsDict.items():
            if build in static.buffs_100:
                for buffedBuild in static.buffs_100[build]:
                    self.buildsDict[build]['buff'][buffedBuild] = 1 + info['star']
            if build in static.buffs_50:
                for buffedBuild in static.buffs_50[build]:
                    self.buildsDict[build]['buff'][buffedBuild] = 1 + info['star'] * 0.5

            if build in static.buffs_ind:
                self.buildsDict[build]['buff']['industry'] = static.buffs_ind[build][info['star'] - 1]
            if build in static.buffs_bus:
                self.buildsDict[build]['buff']['commerce'] = static.buffs_bus[build][info['star'] - 1]
            if build in static.buffs_res:
                self.buildsDict[build]['buff']['residence'] = static.buffs_res[build][info['star'] - 1]

        results = PQ()

        Max = 0
        for buildings in tqdm(searchSpace, total=searchSpaceSize,
                              bar_format='{percentage:3.0f}%,{elapsed}<{remaining}|{bar}|{n_fmt}/{total_fmt},{rate_fmt}{postfix}'):
            TotalIncome, Stat = self.calculateComb(buildings)
            results.put(NamedPQ(-TotalIncome, (buildings, Stat)))

        print("hahahahahaaa")
        Best = results.get()
        print('最优策略：', Best.name[0])
        print('总秒伤：', self.showLetterNum(-Best.priority))

        print('各建筑等级：', [(Best.name[0][i//3][i%3], x) for i, x in enumerate(Best.name[1][0])])
        print('各建筑秒伤：', [(Best.name[0][i//3][i%3], self.showLetterNum(x)) for i, x in enumerate(Best.name[1][1])])

