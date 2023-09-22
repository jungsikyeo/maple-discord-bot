import random
import asyncio
from constants import BOSS_ATTACK_NORMAL, BOSS_ATTACK_AOE, BOSS_ATTACK_DELAY_START, BOSS_ATTACK_DELAY_END
from constants import BOSS_ATTACK_PERCENT_NORMAL, BOSS_ATTACK_PERCENT_AOE, BOSS_MONSTER_LIST


class BossMonster:
    def __init__(self, player_cnt, get_alive_players, game_end, monster_hp_gauge):
        _bosses = BOSS_MONSTER_LIST
        _boss = random.choice(_bosses)
        self.name = _boss['name']
        self.max_hp = _boss['hp'] * player_cnt
        self.current_hp = self.max_hp
        self.get_alive_players = get_alive_players
        self.game_end = game_end
        self.monster_hp_gauge = monster_hp_gauge

    async def attack_players(self, channel):
        while self.current_hp > 0:  # 보스 몬스터가 살아있는 동안 반복
            players = self.get_alive_players()
            if len(players) == 0:  # 살아있는 플레이어가 없을 경우
                await channel.send(content="모든 파티원이 죽었습니다. 보스 공략에 실패했습니다.")
                await self.game_end(channel)
                return
            hp_gauge = self.monster_hp_gauge(self.current_hp, self.max_hp)
            await channel.send(content=f"`{self.name}`가 공격을 준비합니다. HP "
                                       f"[{hp_gauge}]({self.current_hp}/{self.max_hp})",)
            await asyncio.sleep(random.randint(BOSS_ATTACK_DELAY_START, BOSS_ATTACK_DELAY_END))  # 공격 대기
            await self.perform_attack(channel, players)

    async def perform_attack(self, channel, players):
        attack_type = random.choices(
            [BOSS_ATTACK_NORMAL, BOSS_ATTACK_AOE],
            weights=[BOSS_ATTACK_PERCENT_NORMAL, BOSS_ATTACK_PERCENT_AOE],
            k=1
        )[0]

        if attack_type == BOSS_ATTACK_NORMAL:
            target = random.choice(players)
            target.hp = 0  # 플레이어 사망
            await channel.send(f"`{self.name}`이(가) `{target.name}`을(를) 공격하여 사망시켰습니다.")
        elif attack_type == BOSS_ATTACK_AOE:
            targets = random.sample(players, min(5, len(players)))
            target_names = ", ".join([f"`{target.name}`" for target in targets])
            for target in targets:
                target.hp = 0
            await channel.send(f"`{self.name}`의 광역 공격으로 {target_names}이(가) 사망하였습니다.")

    def is_alive(self):
        return self.current_hp > 0
