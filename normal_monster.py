import random
from constants import NORMAL_MONSTER_LIST, NORMAL_MONSTER_BASE_HP


class NormalMonster:
    def __init__(self, player_cnt):
        self.name = random.choice(NORMAL_MONSTER_LIST)
        self.max_hp = NORMAL_MONSTER_BASE_HP * player_cnt
        self.current_hp = self.max_hp

    def is_alive(self):
        return self.current_hp > 0
