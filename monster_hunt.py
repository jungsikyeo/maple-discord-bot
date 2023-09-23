import random
import asyncio
import time
from normal_monster import NormalMonster
from boss_monster import BossMonster
from constants import TOTAL_SPAWNS_COUNT_START, TOTAL_SPAWNS_COUNT_END
from constants import NORMAL_SPAWN_DELAY_START, NORMAL_SPAWN_DELAY_END, BOSS_SPAWN_DELAY_START, BOSS_SPAWN_DELAY_END
from constants import EMBED_HUNT


class MonsterHunt:
    def __init__(self, get_alive_players, game_end, monster_hp_gauge, make_embed):
        self.current_monster = None
        self.spawn_count = 0
        self.total_spawns = random.randint(TOTAL_SPAWNS_COUNT_START, TOTAL_SPAWNS_COUNT_END)
        self.get_alive_players = get_alive_players
        self.game_end = game_end
        self.monster_hp_gauge = monster_hp_gauge
        self.make_embed = make_embed

    async def spawn_monster(self, channel):
        now_in_seconds = time.time()
        now_in_milliseconds = int(now_in_seconds * 1000)

        player_cnt = len(self.get_alive_players())
        if self.spawn_count < self.total_spawns:
            await asyncio.sleep(random.randint(NORMAL_SPAWN_DELAY_START, NORMAL_SPAWN_DELAY_END))
            self.current_monster = NormalMonster(player_cnt)
            hp_gauge = self.monster_hp_gauge(self.current_monster.current_hp, self.current_monster.max_hp)
            embed = self.make_embed({
                'title': f"**{self.current_monster.name}**",
                'description': f"일반 몬스터 **{self.current_monster.name}**이(가) 나타났다! \n"
                               f"HP [{hp_gauge}]({self.current_monster.current_hp}/{self.current_monster.max_hp})",
                'thumbnail_image': f"http://130.162.153.236:9180/static/normal_{self.current_monster.id}.png?v={now_in_milliseconds}",
                'color': EMBED_HUNT,
            })
            await channel.send(embed=embed)
            self.spawn_count += 1
        elif self.spawn_count == self.total_spawns:
            await asyncio.sleep(random.randint(BOSS_SPAWN_DELAY_START, BOSS_SPAWN_DELAY_END))
            self.current_monster = BossMonster(player_cnt, self.get_alive_players, self.game_end, self.monster_hp_gauge, self.make_embed)
            hp_gauge = self.monster_hp_gauge(self.current_monster.current_hp, self.current_monster.max_hp)
            embed = self.make_embed({
                'title': f"**{self.current_monster.name}**",
                'description': f"보스 몬스터 **{self.current_monster.name}**이(가) 나타났다! \n"
                               f"HP [{hp_gauge}]({self.current_monster.current_hp}/{self.current_monster.max_hp})",
                'main_image': f"http://130.162.153.236:9180/static/boss_{self.current_monster.id}.png?v={now_in_milliseconds}",
                'color': EMBED_HUNT,
            })
            await channel.send(embed=embed)
            await self.current_monster.attack_players(channel)
            self.spawn_count += 1
