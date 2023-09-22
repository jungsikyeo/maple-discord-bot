import random
from constants import SKILL_DAMAGE_BASE, SKILL_DAMAGE_CRITICAL


class MagicSkill:
    def __init__(self, name, base_damage):
        self.name = name
        self.base_damage = base_damage

    def compute_damage(self):
        # 여기서는 모든 스킬이 동일한 데미지 메커니즘을 가지도록 합니다.
        # 10% 확률로 크리티컬 데미지
        if random.random() < 0.1:
            return self.base_damage * SKILL_DAMAGE_CRITICAL, 'Critical Hit! '
        return self.base_damage, ''


# 각 마법 스킬 인스턴스 생성
fireball = MagicSkill("Fireball", SKILL_DAMAGE_BASE)
icebolt = MagicSkill("Icebolt", SKILL_DAMAGE_BASE)
lightning = MagicSkill("Lightning", SKILL_DAMAGE_BASE)
earthquake = MagicSkill("Earthquake", SKILL_DAMAGE_BASE)
windblade = MagicSkill("Windblade", SKILL_DAMAGE_BASE)