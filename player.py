import time


class Player:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.hp = 100
        self.accumulated_damage = 0  # 누적 데미지 초기화
        self.magic_attacks_remaining = 3  # 마법 공격 횟수 초기화
        self.defense_mode = False
        self.dead_timestamp = None  # 플레이어 사망 시간 기록

    def is_alive(self):
        return self.hp > 0

    def use_magic_attack(self):
        if self.magic_attacks_remaining > 0:
            self.magic_attacks_remaining -= 1
            return True
        return False

    def die(self):  # 사망 시 호출
        self.hp = 0
        self.dead_timestamp = time.time()  # 사망한 시간 기록

    def can_revive(self):  # 부활 가능 여부 확인
        if self.dead_timestamp and time.time() - self.dead_timestamp >= 5:
            return True
        return False

    def revive(self):  # 부활 로직
        if self.can_revive():
            self.hp = 100
            self.dead_timestamp = None
