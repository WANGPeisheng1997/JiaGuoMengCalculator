class Config:

    def __init__(self):
        # dict of { building_name: { star: int, level: int, buff: int }}
        self.buildings_config = {}

        # dict of { buff_big_type: { buff_small_type: int }}
        # buff_big_type: enum("policy", "album", "mission")
        # buff_small_type: enum("global", "online", "residence", "commerce", "industry", "jiaguozhiguang")
        self.buffs_config = {}

        # list of [ building_name ]
        self.blacklist_config = []

        # list of [ building_name ]
        self.whitelist_config = []

        # string : "3 aa"
        self.gold_config = "0"

        # enum("online", "offline", "train")
        self.mode_config = "online"

        # Bool
        self.only_current = False

    def init_config_from_json(self, json_config):
        self.buildings_config = json_config["buildings"]
        self.buffs_config = json_config["buffs"]
        if "blacklist" in json_config:
            self.blacklist_config = json_config["blacklist"]
        if "whitelist" in json_config:
            self.whitelist_config = json_config["whitelist"]
        if "gold" in json_config:
            self.gold_config = json_config["gold"]
        if "mode" in json_config:
            self.mode_config = json_config["mode"]
        if "only_current" in json_config:
            self.only_current = json_config["only_current"]

    def init_config_from_local(self):
        self.mode_config = 'online'  # 在线模式填online，离线模式填offline，供货模式填train
        self.blacklist_config = '商贸中心 小型公寓 水厂 花园洋房 复兴公馆 加油站 人民石油'.split() # 这里填写不想要或未解锁的建筑
        self.whitelist_config = '商贸中心 复兴公馆 小型公寓 花园洋房'.split() # 这里填写一定要的建筑

        '''
             在这里填写你的建筑的星级
        '''

        BuildStars = {
            5: '人民石油 空中别墅 商贸中心 复兴公馆 纺织厂 图书城 加油站 花园洋房 电厂 小型公寓 居民楼 木屋 五金店 木材厂 食品厂 菜市场 造纸厂 钢结构房 平房 学校 便利店 服装店 水厂',
            4: '零件厂 人才公寓 中式小楼 钢铁厂',
            3: '民食斋 ',
            2: '企鹅机械 媒体之声',
            1: ''
        }

        '''
            在这里填写你的 政策/照片/任务 加成, 单位是百分比
        '''
        Policy = {
            'global': 400,
            'online': 300,
            'offline': 0,
            'residence': 300,
            'commerce': 420,
            'industry': 1500,
            'jiaguozhiguang': 190  # 国庆也填在这！
        }

        Album = {
            'global': 190,
            'online': 160,
            'offline': 200,
            'residence': 210,
            'commerce': 390,
            'industry': 360
        }

        Mission_b = {  # 这里填写任务提供的单建筑加成，如果是100%则填写100
            '便利店': 100,
            '钢铁厂': 0,
            '木材厂': 100,
        }

        Mission_g = {  # 这里填写任务提供的全局加成，如果是100%则填写100
            'global': 0,
            'online': 0,
            'offline': 0,
            'residence': 0,
            'commerce': 0,
            'industry': 0
        }

        '''
            在这里填写你当前的建筑等级
        '''

        Grades = {'中式小楼': 1100,
                  '五金店': 1000,
                  '人才公寓': 1100,
                  '人民石油': 1000,
                  '企鹅机械': 1000,
                  '便利店': 1000,
                  '加油站': 1000,
                  '商贸中心': 1000,
                  '图书城': 1000,
                  '复兴公馆': 1000,
                  '媒体之声': 1050,
                  '学校': 1000,
                  '小型公寓': 1000,
                  '居民楼': 1000,
                  '平房': 1000,
                  '服装店': 1000,
                  '木屋': 1000,
                  '木材厂': 1200,
                  '民食斋': 1100,
                  '水厂': 1000,
                  '电厂': 1000,
                  '空中别墅': 1000,
                  '纺织厂': 1000,
                  '花园洋房': 1000,
                  '菜市场': 1000,
                  '造纸厂': 1000,
                  '钢结构房': 1000,
                  '钢铁厂': 1200,
                  '零件厂': 1200,
                  '食品厂': 1000}
        '''
            在这里填写计划投入的金币数
            格式 数字+单位，比如
            ‘123.456aa’
            可用单位：(G是1, K是1000)
            游戏内金币单位 G K M B T aa bb cc dd ee ff gg hh ii
            建议初次使用金币不超过当前秒伤的1000倍！
        '''

        self.gold_config = '0'

        '''
            以下部分请不要随意改动
        '''

        for star in BuildStars:
            build_list = BuildStars[star].split()
            for build in build_list:
                self.buildings_config[build] = {"star": star, "buff": 0, "level": 0}

        for build in Grades:
            self.buildings_config[build]["level"] = Grades[build]

        for build in Mission_b:
            self.buildings_config[build]["buff"] = Mission_b[build]

        self.buffs_config["policy"] = Policy
        self.buffs_config["album"] = Album
        self.buffs_config["mission"] = Mission_g

