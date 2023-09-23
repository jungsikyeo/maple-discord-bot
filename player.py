class Player:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.hp = 100
        self.accumulated_damage = 0  # 누적 데미지 초기화
        self.magic_attacks_remaining = 3  # 마법 공격 횟수 초기화
        self.defense_mode = False

    def is_alive(self):
        return self.hp > 0

    def use_magic_attack(self):
        if self.magic_attacks_remaining > 0:
            self.magic_attacks_remaining -= 1
            return True
        return False
