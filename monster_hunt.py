import random
import asyncio
from normal_monster import NormalMonster
from boss_monster import BossMonster
from constants import TOTAL_SPAWNS_COUNT_START, TOTAL_SPAWNS_COUNT_END
from constants import NORMAL_SPAWN_DELAY_START, NORMAL_SPAWN_DELAY_END, BOSS_SPAWN_DELAY_START, BOSS_SPAWN_DELAY_END


class MonsterHunt:
    def __init__(self, get_alive_players, game_end, monster_hp_gauge):
        self.current_monster = None
        self.spawn_count = 0
        self.total_spawns = random.randint(TOTAL_SPAWNS_COUNT_START, TOTAL_SPAWNS_COUNT_END)
        self.get_alive_players = get_alive_players
        self.game_end = game_end
        self.monster_hp_gauge = monster_hp_gauge

    async def spawn_monster(self, channel):
        player_cnt = len(self.get_alive_players())
        if self.spawn_count < self.total_spawns:
            await asyncio.sleep(random.randint(NORMAL_SPAWN_DELAY_START, NORMAL_SPAWN_DELAY_END))
            self.current_monster = NormalMonster(player_cnt)
            await channel.send(
                f"일반 몬스터 `{self.current_monster.name}`가 나타났다! HP `{self.current_monster.current_hp}`/`{self.current_monster.max_hp}`")
            self.spawn_count += 1
        elif self.spawn_count == self.total_spawns:
            await asyncio.sleep(random.randint(BOSS_SPAWN_DELAY_START, BOSS_SPAWN_DELAY_END))
            self.current_monster = BossMonster(player_cnt, self.get_alive_players, self.game_end, self.monster_hp_gauge)
            await channel.send(f"보스 몬스터 `{self.current_monster.name}`가 나타났다!")
            await self.current_monster.attack_players(channel)
            self.spawn_count += 1
