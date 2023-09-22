STATUS = 'STATUS'
MSG = 'MSG'

# 게임 입장 시간
JOIN_TIMEOUT = 60 / 10  # 60 * 1

# 플레이어 상태
PLAYER_DIE = {
    STATUS: 'DIE',
    MSG: '당신은 죽었습니다.'
}
PLAYER_ALIVE = {
    STATUS: 'ALIVE',
    MSG: ''
}
PLAYER_NOT_PLAYER = {
    'STATUS': 'NOT_PLAYER',
    MSG: '당신은 파티원이 아닙니다.'
}

# 몬스터 정보
NORMAL_MONSTER_BASE_HP = 100
BOSS_MONSTER_BASE_HP = 1000
NORMAL_MONSTER_LIST = ['Wolf', 'Snail', 'Tino', 'Muru', 'Spore']
BOSS_MONSTER_LIST = [
    {'name': 'Mano', 'hp': int(BOSS_MONSTER_BASE_HP * 0.6)},
    {'name': 'Blue Mushmom', 'hp': int(BOSS_MONSTER_BASE_HP * 0.8)},
    {'name': 'Stumpy', 'hp': BOSS_MONSTER_BASE_HP},
    {'name': 'Crimson Balrog', 'hp': int(BOSS_MONSTER_BASE_HP * 1.2)},
    {'name': 'Dyle', 'hp': int(BOSS_MONSTER_BASE_HP * 1.4)}
]

# 보스 몬스터 기술
BOSS_ATTACK_NORMAL = 'NORMAL'
BOSS_ATTACK_AOE = 'AOE'

# 보스 몬스터 공격 확률
BOSS_ATTACK_PERCENT_NORMAL = 85
BOSS_ATTACK_PERCENT_AOE = 15

# 전체 일반 몬스터 출현 횟수
TOTAL_SPAWNS_COUNT_START = 1  # 3
TOTAL_SPAWNS_COUNT_END = 1  # 5

# 일반 몬스터 출현 대기 시간
NORMAL_SPAWN_DELAY_START = 3
NORMAL_SPAWN_DELAY_END = 6

# 보스 몬스터 출현 대기 시간
BOSS_SPAWN_DELAY_START = 3
BOSS_SPAWN_DELAY_END = 6

# 플레이어 일반 공격 데미지
ATTACK_DAMAGE_START = 10
ATTACK_DAMAGE_END = 30

# 플레이어 스킬 공격 데미지
SKILL_DAMAGE_BASE = 60
SKILL_DAMAGE_CRITICAL = 2

# 보스 몬스터 공격 대기 시간
BOSS_ATTACK_DELAY_START = 5
BOSS_ATTACK_DELAY_END = 10
