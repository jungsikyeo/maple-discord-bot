import random
from constants import NORMAL_MONSTER_LIST


class NormalMonster:
    def __init__(self, player_cnt):
        _normal = random.choice(NORMAL_MONSTER_LIST)
        self.id = _normal['id']
        self.name = _normal['name']
        self.max_hp = _normal['hp'] * player_cnt
        self.current_hp = self.max_hp

    def is_alive(self):
        return self.current_hp > 0
