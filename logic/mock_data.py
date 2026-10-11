# logic/mock_data.py — 假数据/预置数据兜底
# 赛题：药品说明书三行大字卡。
# 本模块的药品数据与 ui/drug_data.py（前端本地副本）采用同一「统一药品形状」，
# 权威源 shared/mock.md（D 维护），代码副本与它逐字一致；py test_ai.py --data 可自检对齐。
# 用途：选常用药（preset 权威数据）+ AI 失败/未配置/超时时降级（mock），保证演示不中断。

import random

# GET /health
MOCK_HEALTH = {"status": "ok"}


# ---------- 统一药品形状（前后端共用，见 shared/contract.md 第 1 节） ----------
# { id, name, lines: {dose, freq, timing}, note, warning }
# id 与素材药盒图 assets/images/box_<id>.jpg 一一对应。
MED_CARDS: dict[str, dict] = {
    "amoxi": {
        "id": "amoxi",
        "name": "阿莫西林胶囊",
        "lines": {"dose": "一次 2 粒", "freq": "一天 3 次", "timing": "饭前饭后都可以，间隔 8 小时"},
        "note": None,
        "warning": "青霉素过敏者禁用",
    },
    "cefix": {
        "id": "cefix",
        "name": "头孢克肟分散片",
        "lines": {"dose": "一次 2 片", "freq": "一天 2 次", "timing": "饭后吃"},
        "note": None,
        "warning": "服药期间和停药 7 天内，一口酒都不能沾",
    },
    "metfor": {
        "id": "metfor",
        "name": "二甲双胍缓释片",
        "lines": {"dose": "一次 1 片", "freq": "一天 2 次", "timing": "随餐或饭后马上吃"},
        "note": "空腹吃容易拉肚子",
        "warning": None,
    },
    "ibu": {
        "id": "ibu",
        "name": "布洛芬缓释胶囊",
        "lines": {"dose": "一次 1 粒", "freq": "一天 2 次", "timing": "饭后吃"},
        "note": "空腹吃伤胃",
        "warning": "有胃病、哮喘请先问医生",
    },
    "nife": {
        "id": "nife",
        "name": "硝苯地平控释片",
        "lines": {"dose": "一次 1 片", "freq": "一天 1 次", "timing": "早晨固定时间，整片吞不能掰"},
        "note": "药片空壳随大便排出是正常的",
        "warning": None,
    },
    "gankang": {
        "id": "gankang",
        "name": "感冒灵颗粒",
        "lines": {"dose": "一次 1 袋", "freq": "一天 3 次", "timing": "开水冲服，饭后"},
        "note": None,
        "warning": "含对乙酰氨基酚，别和其他感冒药一起吃",
    },
    "statin": {
        "id": "statin",
        "name": "阿托伐他汀钙片",
        "lines": {"dose": "一次 1 片", "freq": "一天 1 次", "timing": "睡前吃最好"},
        "note": None,
        "warning": None,
    },
    "amlo": {
        "id": "amlo",
        "name": "氨氯地平片",
        "lines": {"dose": "一次 1 片", "freq": "一天 1 次", "timing": "固定时间，饭前饭后都行"},
        "note": None,
        "warning": None,
    },
}

# GET /medications 目录（由 MED_CARDS 派生，避免两处维护）
MOCK_MEDICATIONS = [{"id": c["id"], "name": c["name"]} for c in MED_CARDS.values()]


def list_medications() -> list[dict]:
    """GET /medications：预置目录。"""
    return MOCK_MEDICATIONS


def get_med_card(drug_id: str) -> dict | None:
    """POST /med-card：按 id 查预置卡；查不到返回 None。"""
    return MED_CARDS.get(drug_id)


def pick_med_card() -> dict:
    """POST /scan 降级：随机给一张预置卡，演示不至于每张一样。"""
    return random.choice(list(MED_CARDS.values()))


# ---------- POST /chat（追问场景，至少 2 条，避免演示重复穿帮） ----------
MOCK_CHAT_REPLIES = [
    "记住三句话：一次 1 片，一天 3 次，饭后吃。记不住就让家人把用药卡拍下来。",
    "饭前忘了吃，想起来就马上补，下一顿照常，千万不要一次吃两片。",
    "药盒上写着每日 3 次、每次 1 片，饭后服用。"
]

# ---------- POST /transcribe ----------
MOCK_TRANSCRIPTS = [
    "这个药饭前吃还是饭后吃？",
    "阿莫西林一天吃几次？",
]

# 异常降级文案：AI 全挂时由前端朗读（shared/mock.md 第 4 节）
MOCK_FALLBACK_MESSAGE = "网络有点慢，我先按最常见的用法告诉你：一次 1 片，一天 3 次，饭后吃。具体请看说明书或咨询药师。"


def pick(options: list[str]) -> str:
    """随机取一条假数据，演示时不至于每次一样。"""
    return random.choice(options)
