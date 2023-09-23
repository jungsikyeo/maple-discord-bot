STATUS = 'STATUS'
MSG = 'MSG'

# 게임 입장 시간
JOIN_TIMEOUT = 60 / 5 # 60 * 1

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
NORMAL_MONSTER_LIST = [
    # {'name': 'Wolf', 'hp': NORMAL_MONSTER_BASE_HP},
    # {'name': 'Snail', 'hp': NORMAL_MONSTER_BASE_HP},
    # {'name': 'Tino', 'hp': NORMAL_MONSTER_BASE_HP},
    # {'name': 'Muru', 'hp': NORMAL_MONSTER_BASE_HP},
    # {'name': 'Spore', 'hp': NORMAL_MONSTER_BASE_HP}
    {
        'id': 1,
        'name': '고블린',
        'hp': NORMAL_MONSTER_BASE_HP
    },
    {
        'id': 2,
        'name': '블러드 엘프',
        'hp': NORMAL_MONSTER_BASE_HP
    },
    {
        'id': 3,
        'name': '트롤',
        'hp': NORMAL_MONSTER_BASE_HP
    },
    {
        'id': 4,
        'name': '타우렌',
        'hp': NORMAL_MONSTER_BASE_HP
    },
    {
        'id': 5,
        'name': '언데드',
        'hp': NORMAL_MONSTER_BASE_HP
    },
    {
        'id': 6,
        'name': '오크',
        'hp': NORMAL_MONSTER_BASE_HP
    }
]
BOSS_MONSTER_LIST = [
    # {'name': 'Mano', 'hp': int(BOSS_MONSTER_BASE_HP * 0.6)},
    # {'name': 'Blue Mushmom', 'hp': int(BOSS_MONSTER_BASE_HP * 0.8)},
    # {'name': 'Stumpy', 'hp': BOSS_MONSTER_BASE_HP},
    # {'name': 'Crimson Balrog', 'hp': int(BOSS_MONSTER_BASE_HP * 1.2)},
    # {'name': 'Dyle', 'hp': int(BOSS_MONSTER_BASE_HP * 1.4)}
    {
        'id': 1,
        'name': '라그나로스',
        'hp': int(BOSS_MONSTER_BASE_HP * 0.6),
        'normal': ['망치질', '화염 충격', '화염의 검'],
        'magic': ['화염의 소용돌이', '용암 폭발', '용암 파도']
    },
    {
        'id': 2,
        'name': '네파리안',
        'hp': int(BOSS_MONSTER_BASE_HP * 0.8),
        'normal': ['발톱 공격', '꼬리 휩쓸기', '비명'],
        'magic': ['어둠의 숨결', '어둠의 충격', '용의 눈물']
    },
    {
        'id': 3,
        'name': '켈투자드',
        'hp': int(BOSS_MONSTER_BASE_HP * 1.0),
        'normal': ['얼음 창', '얼음 파편', '냉기의 휩쓸기'],
        'magic': ['얼어붙은 땅', '얼음의 소용돌이', '냉기의 숨결']
    },
    {
        'id': 4,
        'name': '프린스 말체자르',
        'hp': int(BOSS_MONSTER_BASE_HP * 1.2),
        'normal': ['지옥의 검', '암흑의 찌르기', '암흑의 폭풍'],
        'magic': ['불안정한 파멸', '암흑의 불길', '지옥의 불길']
    },
    {
        'id': 5,
        'name': '킬제덴',
        'hp': int(BOSS_MONSTER_BASE_HP * 0.8),
        'normal': ['지옥의 갈퀴', '악마의 칼날', '암흑의 일격'],
        'magic': ['불타는 불꽃', '악마의 숨결', '지옥의 포화']
    },
    {
        'id': 6,
        'name': '리치 왕',
        'hp': int(BOSS_MONSTER_BASE_HP * 1.6),
        'normal': ['냉기의 일격', '죽음의 충격', '냉기의 찌르기'],
        'magic': ['영혼의 포화', '냉기의 소용돌이', '죽음의 재생']
    },
    {
        'id': 7,
        'name': '블랙핸드',
        'hp': int(BOSS_MONSTER_BASE_HP * 0.5),
        'normal': ['대검 휘두르기', '철갑 박치기', '용암의 일격'],
        'magic': ['용암 폭발', '용의 눈물', '화염의 폭풍']
    },
    {
        'id': 8,
        'name': '굴단',
        'hp': int(BOSS_MONSTER_BASE_HP * 1.2),
        'normal': ['지옥의 망치', '어둠의 찌르기', '지옥의 일격'],
        'magic': ['어둠의 방출', '악마의 폭발', '지옥의 소용돌이']
    }
]

# 보스 몬스터 기술
BOSS_ATTACK_NORMAL = '공격'
BOSS_ATTACK_AOE = '광역 공격'

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

# Embed 색상
EMBED_ERROR = 0xff0000
EMBED_JOIN = 0xEFB90A
EMBED_HUNT = 0x37e37b
