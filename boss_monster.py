import random
import asyncio
from constants import BOSS_ATTACK_NORMAL, BOSS_ATTACK_AOE, BOSS_ATTACK_DELAY_START, BOSS_ATTACK_DELAY_END
from constants import BOSS_ATTACK_PERCENT_NORMAL, BOSS_ATTACK_PERCENT_AOE, BOSS_MONSTER_LIST
from constants import EMBED_HUNT


class BossMonster:
    def __init__(self, player_cnt, get_alive_players, game_end, monster_hp_gauge, make_embed, get_game_playing):
        _boss = random.choice(BOSS_MONSTER_LIST)
        self.id = _boss['id']
        self.name = _boss['name']
        self.max_hp = _boss['hp'] * player_cnt
        self.current_hp = self.max_hp
        self.normal_attacks = _boss['normal']
        self.magic_attacks = _boss['magic']
        self.get_alive_players = get_alive_players
        self.game_end = game_end
        self.monster_hp_gauge = monster_hp_gauge
        self.make_embed = make_embed
        self.get_game_playing = get_game_playing

    async def attack_players(self, channel):
        while self.current_hp > 0:  # 보스 몬스터가 살아있는 동안 반복
            if not self.get_game_playing():
                return
            players = self.get_alive_players()
            if len(players) == 0:  # 살아있는 플레이어가 없을 경우
                embed = self.make_embed({
                    'title': '보스 공략 실패',
                    'description': "모든 파티원이 죽었습니다. 보스 공략에 실패했습니다.",
                    'color': EMBED_HUNT,
                })
                await channel.send(embed=embed)
                await self.game_end(channel)
                return
            else:
                await asyncio.sleep(random.randint(BOSS_ATTACK_DELAY_START, BOSS_ATTACK_DELAY_END))  # 공격 대기
            attack_type = random.choices(
                [BOSS_ATTACK_NORMAL, BOSS_ATTACK_AOE],
                weights=[BOSS_ATTACK_PERCENT_NORMAL, BOSS_ATTACK_PERCENT_AOE],
                k=1
            )[0]
            if attack_type == BOSS_ATTACK_NORMAL:
                target_msg = "누군가를 노려보고 있습니다!"
            else:
                target_msg = "무언가를 준비하고 있습니다!"
            hp_gauge = self.monster_hp_gauge(self.current_hp, self.max_hp, 20)
            embed = self.make_embed({
                'title': '경고!',
                'description': f"```diff\n"
                               f"-{self.name}이(가) {target_msg}"
                               f"```\n"
                               f"HP [{hp_gauge}]",
                'color': EMBED_HUNT,
            })
            await channel.send(embed=embed)
            await asyncio.sleep(random.randint(BOSS_ATTACK_DELAY_START, BOSS_ATTACK_DELAY_END))  # 공격 대기
            await self.perform_attack(channel, players, attack_type)

    async def perform_attack(self, channel, players, attack_type):
        if attack_type == BOSS_ATTACK_NORMAL:
            target = random.choice(players)
            normal_attack = random.choice(self.normal_attacks)
            description = f"<:attack_1:1155149010550657124> | **{self.name}**이(가) **{target.name}**에게 공격을 시도합니다.\n"
            if target.defense_mode:
                description += f"<:defense_1:1155844018639482950> | **{target.name}**은(는) **{self.name}**의 **{normal_attack}**을(를) 회피하였습니다."
                target.defense_mode = False
            else:
                description += f"<:attack_2:1155149012501020692> | **{self.name}**이(가) **{target.name}**에게 **{normal_attack}**을(를) 시전하여 사망시켰습니다."
                target.die()
            embed = self.make_embed({
                'description': description,
                'color': EMBED_HUNT,
            })
            await channel.send(embed=embed)
        elif attack_type == BOSS_ATTACK_AOE:
            targets = random.sample(players, min(5, len(players)))
            magic_attack = random.choice(self.magic_attacks)
            target_alive_names = ""
            target_die_names = ""
            for target in targets:
                if target.defense_mode:
                    target_alive_names += f"{target.name}, "
                    target.defense_mode = False
                else:
                    target_die_names += f"{target.name}, "
                    target.die()
            description = f"<:skill_2:1155149046923661433> | **{self.name}**이(가) 광역 스킬 **{magic_attack}**을 시전합니다.\n"
            if target_die_names:
                description += f"<:attack_2:1155149012501020692> | **{self.name}**의 **{magic_attack}** 광역 공격으로 {target_die_names[:-2]}이(가) 사망하였습니다.\n"
            if target_alive_names:
                description += f"<:defense_1:1155844018639482950> | **{target_alive_names[:-2]}**은(는) **{self.name}**의 **{magic_attack}** 광역 공격을 회피하였습니다."
            embed = self.make_embed({
                'title': f"{magic_attack}",
                'description': description,
                'color': EMBED_HUNT,
            })
            await channel.send(embed=embed)

    def is_alive(self):
        return self.current_hp > 0
