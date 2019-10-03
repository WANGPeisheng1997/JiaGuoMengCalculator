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
        self.mode = "online"

    def init_config_from_json(self, json_config):
        self.buildings_config = json_config["buildings"]
        self.buffs_config = json_config["buffs"]
        if "blacklist" in json_config:
            self.blacklist_config = json_config["blacklist"]
        if "whitelist" in json_config:
            self.whitelist_config = json_config["whitelist"]
        if "gold" in json_config:
            self.whitelist_config = json_config["gold"]
        if "mode" in json_config:
            self.whitelist_config = json_config["mode"]
