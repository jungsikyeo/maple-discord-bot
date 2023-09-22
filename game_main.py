import discord
import os
import asyncio
import random
import time
from constants import STATUS, MSG
from constants import PLAYER_DIE, PLAYER_ALIVE, PLAYER_NOT_PLAYER
from constants import JOIN_TIMEOUT, TOTAL_SPAWNS_COUNT_START, TOTAL_SPAWNS_COUNT_END
from constants import ATTACK_DAMAGE_START, ATTACK_DAMAGE_END
from skills import fireball, icebolt, lightning, earthquake, windblade
from monster_hunt import MonsterHunt
from boss_monster import BossMonster
from player import Player
from discord.ui import button, View
from discord import ButtonStyle, Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
command_flag = os.getenv("SEARCHFI_BOT_FLAG")
bot = commands.Bot(command_prefix=command_flag, intents=discord.Intents.all())

guild_ids = [1069466891367751691]
magic_skills = [fireball, icebolt, lightning, earthquake, windblade]

participating_players = set()  # 참여하는 플레이어들의 집합
monster_spawn_count = 0  # 일반몬스터 개체 수
game_playing = False  # 게임 진행중 여부
last_attack_time = {}  # 각 사용자의 마지막 공격 시간을 저장하는 딕셔너리
user_damage_accumulation = {}  # 각 사용자의 누적 데미지를 저장하는 딕셔너리


def make_embed(embed_info):
    embed = Embed(
        title=embed_info.get('title', ''),
        description=embed_info.get('description', ''),
        color=embed_info.get('color', 0xFFFFFF),
    )
    if embed_info.get('image_url', None):
        embed.set_image(
            url=embed_info.get('image_url')
        )
    embed.set_footer(text="Powered by SearchFi")
    return embed

class JoinGameView(View):
    def __init__(self):
        super().__init__(timeout=JOIN_TIMEOUT)

    @button(label="게임 참여 (0/100)", style=ButtonStyle.primary)
    async def join_game(self, _, interaction):
        global participating_players

        try:
            # 이미 참여한 유저 제외
            for player in participating_players:
                if player.id == interaction.user.id:
                    await interaction.response.send_message(content=f"`{interaction.user.name}`님은 이미 파티원입니다.",
                                                            ephemeral=True)
                    return

            # 참여자 100명 초과 시 참전 불가
            if len(participating_players) >= 100:
                await interaction.response.send_message(f"파티원 구성이 마감되었습니다.", ephemeral=True)

            # 참여자 등록
            participating_players.add(Player(interaction.user))
            await interaction.response.send_message(content=f"`{interaction.user.name}`님이 파티에 가입하였습니다.",
                                                    ephemeral=True)

            # 버튼 레이블 업데이트
            self.join_game.label = f"게임 참여 ({len(participating_players)}/100)"
            await interaction.message.edit(view=self)
        except Exception as e:
            print(e)


def get_alive_players():
    global participating_players
    return [player for player in participating_players if player.is_alive()]


async def game_end(ctx):
    global game_playing
    if game_playing:
        await ctx.send(content="게임이 종료되었습니다.")
        await reset()


def monster_hp_gauge(current_hp, max_hp):
    hp_percentage = current_hp / max_hp
    hp_gauge = "█" * int(hp_percentage * 10) + "▒" * (10 - int(hp_percentage * 10))
    return hp_gauge


# 게임 클래스 생성
game = MonsterHunt(get_alive_players, game_end, monster_hp_gauge)


@bot.command()
async def mud_start(ctx):
    try:
        if ctx.message.author.guild_permissions.administrator:  # 사용자가 관리자 권한을 가지고 있는지 확인
            global game_playing, participating_players, game

            participating_players.clear()

            if game_playing:
                await ctx.send(content="이미 게임이 진행중입니다.")
                return

            join_message = await ctx.send(content=f"{int(JOIN_TIMEOUT/60)}분 동안 파티원을 모집합니다! 아래 버튼을 클릭하여 게임에 참여해주세요.",
                                          view=JoinGameView())
            await asyncio.sleep(JOIN_TIMEOUT)
            await join_message.edit(content="파티원 모집이 종료되었습니다.", view=None)

            if len(participating_players) > 0:
                game_playing = True
            else:
                game_playing = False
                await ctx.send(content="파티원이 구성되지 않았습니다.")
                await game_end(ctx)
                return

            # 게임 시작 알림
            await ctx.send("게임을 시작합니다.")
            game.spawn_count = 0
            game.total_spawns = random.randint(TOTAL_SPAWNS_COUNT_START, TOTAL_SPAWNS_COUNT_END)
            await game.spawn_monster(ctx.channel)
        else:
            await ctx.reply(content="관리자만 사용가능합니다.", mention_author=True)
            await ctx.message.delete()
    except Exception as e:
        print(e)
        await stop(ctx)


async def player_check(ctx):
    global participating_players

    for player in participating_players:
        if player.id == ctx.author.id:
            if not player.is_alive():
                return PLAYER_DIE, None
            else:
                return PLAYER_ALIVE, player
    return PLAYER_NOT_PLAYER, None


@bot.slash_command(
    name="attack",
    description="Player - Attack Monster",
    guild_ids=guild_ids
)
async def attack(ctx):
    try:
        global game, last_attack_time

        user_id = ctx.author.id
        now = time.time()  # 현재 시간

        # 사용자가 최근에 공격한 시간이 기록되어 있고, 그로부터 3초 이내인 경우
        if user_id in last_attack_time and now - last_attack_time[user_id] < 3:
            await ctx.respond(content="3초 이내에는 입력할 수 없습니다. 잠시후 시도해주세요.", ephemeral=True)
            return

        # 마지막 공격 시간 갱신
        last_attack_time[user_id] = now

        # 파티원인지 확인
        check_result, current_player = await player_check(ctx)

        # 생존해있는 파티원만 공격 가능
        if check_result[STATUS] == PLAYER_ALIVE[STATUS]:
            if game.current_monster:
                if game.current_monster.is_alive():
                    damage = random.randint(ATTACK_DAMAGE_START, ATTACK_DAMAGE_END)
                    game.current_monster.current_hp -= damage
                    current_player.accumulated_damage += damage
                    if not game.current_monster.is_alive():
                        current_player.accumulated_damage += game.current_monster.current_hp  # 마이너스 HP인 경우 누적 데미지 보정
                        game.current_monster.current_hp = 0
                        await ctx.respond(content=f"`{game.current_monster.name}`가 죽었습니다.",
                                          ephemeral=True)
                        await ctx.respond(content=f"`{ctx.author.name}`가 `{game.current_monster.name}`를 처치했다! "
                                                  f"`{ctx.author.name}`의 누적 데미지 `{current_player.accumulated_damage}`")
                        if isinstance(game.current_monster, BossMonster):
                            await game_end(ctx)
                        else:
                            await game.spawn_monster(ctx.channel)
                    else:
                        hp_gauge = monster_hp_gauge(game.current_monster.current_hp, game.current_monster.max_hp)
                        await ctx.respond(content=f"`{game.current_monster.name}`에게 공격 성공! "
                                                  f"`{game.current_monster.name}` HP "
                                                  f"[{hp_gauge}]({game.current_monster.current_hp}/{game.current_monster.max_hp})",
                                          ephemeral=True
                                          )
                else:
                    await ctx.respond(content="공격 대상이 없습니다.", ephemeral=True)
            else:
                await ctx.respond(content="공격 대상이 없습니다.", ephemeral=True)
        else:
            await ctx.respond(content=check_result[MSG], ephemeral=True)
    except Exception as e:
        print(e)
        await stop(ctx)


@bot.slash_command(
    name="skill",
    description="Player - Magic Attack Monster",
    guild_ids=guild_ids
)
async def skill(ctx):
    try:
        global game, last_attack_time

        user_id = ctx.author.id
        now = time.time()  # 현재 시간

        # 사용자가 최근에 공격한 시간이 기록되어 있고, 그로부터 3초 이내인 경우
        if user_id in last_attack_time and now - last_attack_time[user_id] < 3:
            await ctx.respond(content="3초 이내에는 입력할 수 없습니다. 잠시후 시도해주세요.", ephemeral=True)
            return

        # 마지막 공격 시간 갱신
        last_attack_time[user_id] = now

        # 파티원인지 확인
        check_result, current_player = await player_check(ctx)

        # 생존해있는 파티원만 공격 가능
        if check_result[STATUS] == PLAYER_ALIVE[STATUS]:
            if game.current_monster:
                if game.current_monster.is_alive():
                    if not current_player.use_magic_attack():
                        await ctx.respond(content="마법 공격 횟수를 모두 사용했습니다.", ephemeral=True)
                        return
                    chosen_skill = random.choice(magic_skills)
                    damage, critical_msg = chosen_skill.compute_damage()

                    game.current_monster.current_hp -= damage
                    current_player.accumulated_damage += damage

                    if not game.current_monster.is_alive():
                        current_player.accumulated_damage += game.current_monster.current_hp  # 마이너스 HP인 경우 누적 데미지 보정
                        game.current_monster.current_hp = 0
                        await ctx.respond(content=f"`{game.current_monster.name}`가 죽었습니다.",
                                          ephemeral=True)
                        await ctx.respond(
                            content=f"`{ctx.author.name}`가 `{chosen_skill.name}` 마법으로 `{game.current_monster.name}`를 처치했다! "
                                    f"`{ctx.author.name}`의 누적 데미지 `{current_player.accumulated_damage}`")
                        if isinstance(game.current_monster, BossMonster):
                            await game_end(ctx)
                        else:
                            await game.spawn_monster(ctx.channel)
                    else:
                        hp_gauge = monster_hp_gauge(game.current_monster.current_hp, game.current_monster.max_hp)
                        await ctx.respond(
                            content=f"{critical_msg}`{ctx.author.name}`가 `{chosen_skill.name}` 마법으로 `{game.current_monster.name}`에게 공격 성공! "
                                    f"`{game.current_monster.name}` HP "
                                    f"[{hp_gauge}]({game.current_monster.current_hp}/{game.current_monster.max_hp})",
                            ephemeral=True
                        )
                else:
                    await ctx.respond(content="공격 대상이 없습니다.", ephemeral=True)
            else:
                await ctx.respond(content="공격 대상이 없습니다.", ephemeral=True)
        else:
            await ctx.respond(content=check_result[MSG], ephemeral=True)
    except Exception as e:
        print(e)
        await stop(ctx)


async def reset():
    global game_playing, participating_players, monster_spawn_count, last_attack_time, user_damage_accumulation
    participating_players.clear()
    monster_spawn_count = 0
    game_playing = False
    last_attack_time.clear()
    user_damage_accumulation.clear()


@bot.command()
async def stop(ctx):
    global game_playing
    if game_playing:
        await ctx.send(content="예기치 못한 오류가 발생되어 게임을 중지합니다. 이번 라운드의 모든 행위는 기록되지 않습니다.")
        await asyncio.sleep(2)
        await ctx.send(content="게임이 종료되었습니다.")
        await reset()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected!')


bot.run(bot_token)