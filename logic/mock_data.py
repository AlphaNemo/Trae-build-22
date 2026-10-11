# logic/mock_data.py — 假数据/预置数据兜底
# 预置常用药三行卡（赛题要求：阿莫西林、二甲双胍、布洛芬）。
# mock.md 由 D 对照 shared/contract.md 维护，B 负责代码侧与之一致。
# 用途：选常用药（preset 权威数据）+ AI 失败/未配置/超时时降级（mock），保证演示不中断。

import random

# GET /health
MOCK_HEALTH = {"status": "ok"}

# ---------- 预置常用药（离线可用，source=preset；降级时也复用，source=mock） ----------
MOCK_MEDICATIONS = [
    {"id": "amoxicillin", "name": "阿莫西林"},
    {"id": "metformin", "name": "二甲双胍"},
    {"id": "ibuprofen", "name": "布洛芬"},
]

MED_CARDS: dict[str, dict] = {
    "amoxicillin": {
        "drug_name": "阿莫西林",
        "per_dose": "一次 1 片",
        "daily_times": "一天 3 次",
        "meal_timing": "饭后吃",
        "speak_text": "阿莫西林：一次吃 1 片，一天吃 3 次，饭后吃。阿莫西林是抗生素，请按医生交代吃完疗程，不要自己停药。",
        "share_text": "【用药卡】阿莫西林：一次 1 片，一天 3 次，饭后吃。请遵医嘱吃完疗程。",
    },
    "metformin": {
        "drug_name": "二甲双胍",
        "per_dose": "一次 1 片",
        "daily_times": "一天 2 次",
        "meal_timing": "随餐吃",
        "speak_text": "二甲双胍：一次吃 1 片，一天吃 2 次，跟着饭一起吃，可以减少胃部不舒服。",
        "share_text": "【用药卡】二甲双胍：一次 1 片，一天 2 次，随餐吃。胃部不适请咨询医生。",
    },
    "ibuprofen": {
        "drug_name": "布洛芬",
        "per_dose": "一次 1 片",
        "daily_times": "一天 3 次",
        "meal_timing": "饭后吃",
        "speak_text": "布洛芬：一次吃 1 片，一天吃 3 次，饭后吃，不要空腹吃。最多连吃 3 天，不见好要去看医生。",
        "share_text": "【用药卡】布洛芬：一次 1 片，一天 3 次，饭后吃。不要空腹服，连用不超过 3 天。",
    },
}


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
