import numpy as np
import unicodedata
from tqdm import tqdm
import itertools
from queue import PriorityQueue as PQ
from scipy.special import comb
from collections import defaultdict as ddict

#======= 配置：在这里输入自己的状况 =======
Mode = 'Online'
last_result=(('人才公寓', '木屋', '居民楼'), ('五金店', '菜市场', '便利店'), ('食品厂', '电厂', '木材厂'))

# 在这里填写你各建筑的星数。
OneStars = '人民石油'
TwoStars = '空中别墅 商贸中心 复兴公馆 媒体之声 企鹅机械'
TriStars = '民食斋 钢铁厂 人才公寓 中式小楼 加油站 花园洋房'
QuaStars = '纺织厂 图书城 零件厂'
PenStars = '电厂 小型公寓 居民楼 木屋 五金店 木材厂 食品厂 菜市场 造纸厂 钢结构房 平房 学校 便利店 服装店 水厂'

# 在这里填写你的政策加成。
# 没加成为0，有100%加成为1，有150%加成为1.5，以此类推。
Policy = {
    'Global':  6,
    'Online':  2,
    'Offline': 0,
    'Residence': 3,
    'Commercial': 9,
    'Industry': 9,
    'JiaGuoZhiGuang': 0.9
}

# 在这里填写你的照片加成。
# 数字的意义见上。
Photos = {
    'Global':  1.4,
    'Online':  1.4,
    'Offline': 0.7,
    'Residence': 2.4,
    'Commercial': 3,
    'Industry': 2.1,
}

# 在这里填写你的城市任务加成。
# 数字的意义见上。
QuestsGeneral = {
    'Global':  0,
    'Online':  0,
    'Offline': 0,
    'Residence': 0,
    'Commercial': 0,
    'Industry': 0,
}
QuestsBuilding = {
    '花园洋房': 0,
    '空中别墅': 0,
    '复兴公馆': 0,
    '商贸中心': 0,
    '加油站': 0,
    '人民石油': 0,
    '媒体之声': 0,
    '企鹅机械': 0,
    '中式小楼': 0,
    '零件厂': 0,
    '人才公寓': 0,
    '民食斋': 0,
    '纺织厂': 1,
    '图书城': 2,
    '水厂': 0,
    '电厂': 0,
    '钢铁厂': 1,
    '小型公寓': 0,
    '服装店': 0,
    '木材厂': 2,
    '木屋': 0,
    '菜市场': 0,
    '食品厂': 0,
    '钢结构房': 0,
    '造纸厂': 0,
    '便利店': 0,
    '五金店': 0,
    '平房': 0,
    '居民楼': 0,
    '学校': 0,
}

#======= 结束配置 =======

commercial = '便利店 五金店 服装店 菜市场 学校 图书城 商贸中心 加油站 民食斋 媒体之声'
residence = '木屋 居民楼 钢结构房 平房 小型公寓 人才公寓 花园洋房 中式小楼 空中别墅 复兴公馆'
industry  = '木材厂 食品厂 造纸厂 水厂 电厂 钢铁厂 纺织厂 零件厂 企鹅机械 人民石油'

class UndefinedError(Exception): pass

if Mode == 'Online':
    BlackList=set(' 小型公寓 复兴公馆 水厂'.split())
elif Mode == 'Offline':
# TODO:
    raise UndefinedError('离线收益等我有空再写，真的用得到吗')
    BlackList=set(' 小型公寓 电厂'.split())

ListDifference=lambda a,b: [item for item in a if not item in b]
commercial=ListDifference(commercial.split(),BlackList)
residence=ListDifference(residence.split(),BlackList)
industry=ListDifference(industry.split(),BlackList)

OneStars=ListDifference(OneStars.split(),BlackList)
TwoStars=ListDifference(TwoStars.split(),BlackList)
TriStars=ListDifference(TriStars.split(),BlackList)
QuaStars=ListDifference(QuaStars.split(),BlackList)
PenStars=ListDifference(PenStars.split(),BlackList)

#
star = dict()
for item in OneStars:
    star[item] = 1
for item in TwoStars:
    star[item] = 2
for item in TriStars:
    star[item] = 3
for item in QuaStars:
    star[item] = 4
for item in PenStars:
    star[item] = 5

startDict = {1:1, 2:2, 3:6, 4:24, 5:120}

######星级 * 政策 * 照片 * 任务
start = ddict(int)
for item in residence:#住宅
    start[item] = (startDict[star[item]] *
        (1+Policy['Global']+Policy['Online']+Policy['Residence']+Policy['JiaGuoZhiGuang']) *
        (1+Photos['Global']+Photos['Online']+Photos['Residence']) *
        (1+QuestsGeneral['Global']+QuestsGeneral['Online']+QuestsGeneral['Residence']+QuestsBuilding.get(item, 0))
    )
for item in commercial:#商业
    start[item] = (startDict[star[item]] *
        (1+Policy['Global']+Policy['Online']+Policy['Commercial']+Policy['JiaGuoZhiGuang']) *
        (1+Photos['Global']+Photos['Online']+Photos['Commercial']) *
        (1+QuestsGeneral['Global']+QuestsGeneral['Online']+QuestsGeneral['Commercial']+QuestsBuilding.get(item, 0))
    )
for item in industry:#工业
    start[item] = (startDict[star[item]] *
        (1+Policy['Global']+Policy['Online']+Policy['Industry']+Policy['JiaGuoZhiGuang']) *
        (1+Photos['Global']+Photos['Online']+Photos['Industry']) *
        (1+QuestsGeneral['Global']+QuestsGeneral['Online']+QuestsGeneral['Industry']+QuestsBuilding.get(item, 0))
    )

# 自带调整
start['花园洋房'] *= 1.022
start['商贸中心'] *= 1.022
start['平房'] *= 1.097
start['电厂'] *= 1.18
#start['水厂'] *= 1.26
start['加油站'] *= 1.2
start['企鹅机械'] *= 1.33
start['人才公寓'] *= 1.4
start['中式小楼'] *= 1.4
start['民食斋'] *= 1.52
start['空中别墅'] *= 1.52
start['媒体之声'] *= 1.615

buffs_100 = {
    '木屋': ['木材厂'],
    '居民楼': ['便利店'],
    '钢结构房': ['钢铁厂'],
    '花园洋房': ['商贸中心'],
    '空中别墅': ['民食斋'],
    '便利店': ['居民楼'],
    '五金店': ['零件厂'],
    '服装店': ['纺织厂'],
    '菜市场': ['食品厂'],
    '学校':  ['图书城'],
    '图书城': ['学校', '造纸厂'],
    '商贸中心': ['花园洋房'],
    '木材厂': ['木屋'],
    '食品厂': ['菜市场'],
    '造纸厂': ['图书城'],
    '钢铁厂': ['钢结构房'],
    '纺织厂': ['服装店'],
    '零件厂': ['五金店'],
    '企鹅机械':['零件厂'],
    '人民石油':['加油站'],
}

buffs_50 = {
    '零件厂': ['企鹅机械'],
    '加油站': ['人民石油'],
}

bufflist_258 = [.2, .5, .8, 1.1, 1.4]
bufflist_246 = [.2, .4, .6, .8, 1.0]
bufflist_015 = [0.75*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_010 = [0.5*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_005 = [0.25*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_035 = [1.75*x for x in [.2, .4, .6, .8, 1.0]]

buffs_com = {
    '媒体之声': bufflist_005,
    '企鹅机械': bufflist_015,
    '民食斋': bufflist_246,
    '纺织厂': bufflist_015,
    '人才公寓': bufflist_246,
    '中式小楼': bufflist_246,
    '空中别墅': bufflist_258,
    '电厂': bufflist_258,
}
buffs_ind = {
    '媒体之声': bufflist_005,
    '钢铁厂': bufflist_015,
    '中式小楼': bufflist_246,
    '民食斋': bufflist_246,
    '空中别墅': bufflist_258,
    '电厂': bufflist_258,
    '企鹅机械': bufflist_258,
    '人才公寓': bufflist_035,
}
buffs_res = {
    '媒体之声': bufflist_005,
    '企鹅机械':bufflist_010,
    '民食斋': bufflist_246,
    '人才公寓': bufflist_246,
    '平房': bufflist_246,
    '空中别墅': bufflist_258,
    '电厂': bufflist_258,
    '中式小楼': bufflist_035,
}

def calculateComb(buildings):
    buildtuple = buildings[0] + buildings[1] + buildings[2]
    starts = [start[x] for x in buildtuple]
    results = [1] * 9
    for item in buildtuple:
        if item in buffs_100:
            for buffed in buffs_100[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item]
        if item in buffs_50:
            for buffed in buffs_50[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item]*0.5
        if item in buffs_com:
            toAdd = buffs_com[item][star[item]-1]
            results[0] += toAdd
            results[1] += toAdd
            results[2] += toAdd
        if item in buffs_ind:
            toAdd = buffs_ind[item][star[item]-1]
            results[3] += toAdd
            results[4] += toAdd
            results[5] += toAdd
        if item in buffs_res:
            toAdd = buffs_res[item][star[item]-1]
            results[6] += toAdd
            results[7] += toAdd
            results[8] += toAdd
    return (np.sum([v*results[i] for i, v in enumerate(starts)]),
            [v*results[i]/startDict[star[buildtuple[i]]] for i, v in enumerate(starts)])

#
results = PQ()
#
class Result(object):
    def __init__(self, priority, builds):
        self.priority = priority
        self.builds = builds
        return
    def __lt__(self, other):
        return self.priority < other.priority
    def __eq__(self, other):
        return self.priority == other.priority

search_space=itertools.product(itertools.combinations(residence, 3), itertools.combinations(commercial, 3), itertools.combinations(industry, 3))
search_space_size=comb(len(industry), 3)*comb(len(commercial), 3)*comb(len(residence), 3)
print('Total iterations:', search_space_size)
for item in tqdm(search_space,total=search_space_size,bar_format='{percentage:3.0f}%, {elapsed}<{remaining}|{bar}|{n_fmt}/{total_fmt}, {rate_fmt}{postfix}',ncols=70):
    prod = calculateComb(item)
#    if prod > Max:
#        print('\n', prod, item)
#        Max = prod
    results.put(Result(-prod[0], (item, prod[1])))
    pass

def printTable(content):
    def strwid(string):
        return sum(
            2 if unicodedata.east_asian_width(char) in {'W', 'F' and 'A'}
            else 1
            for char in string
        )

    widths = [max(strwid(cell) for cell in col) for col in zip(*content)]
    for row in content:
        printed_cells = (
            ' ' * (width - strwid(cell)) + cell
            for cell, width in zip(row, widths)
        )
        print(' | '.join(printed_cells))



cdict = dict()
#for i in range(2):
#    cdict[i] = results.get()
#    print(-cdict[i].priority, cdict[i].builds)
layout, scores = results.get().builds
layout_list = [cell for row in layout for cell in row]
priorities = [x*startDict[star[layout_list[i]]] for i, x in enumerate(scores)]
printTable([
    ['#'] + ['{}'.format(d) for d in range(9)],
    ['最优策略'] + layout_list,
    ['各建筑加成倍率'] + ['{:.2f}'.format(score) for score in scores],
    ['升级优先级'] + ['{:.2f}'.format(priority) for priority in priorities],
])
print('总加成倍率：{:.2f}'.format(sum(priorities)))

def getNext():
    print('==============')
    Rec = results.get()
    print('次优策略：', Rec.builds[0])
    print('总加成倍率', np.round(sum(priorities), 2))
    print('各建筑加成倍率', np.round(Rec.builds[1], 2))
    print('升级优先级', np.round(priorities, 2))

last_result=[list(item) for item in last_result]
now_result=[list(item) for item in layout]
for class_num in range(3):
    for item in last_result[class_num][:]:
        if item in now_result[class_num]:
            last_result[class_num].remove(item)
            now_result[class_num].remove(item)
print(last_result,'被')
print(now_result,'替换')

upgrade_order=np.argsort(priorities)[::-1]
print('升级顺序:({})'.format(', '.join(
    layout_list[i] for i in upgrade_order
)))