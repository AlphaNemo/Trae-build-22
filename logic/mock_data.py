# logic/mock_data.py — 假数据/预置数据兜底
# 预置常用药三行卡（赛题要求：阿莫西林、二甲双胍、布洛芬）。
# mock.md 由 D 对照 shared/contract.md 维护，B 负责代码侧与之一致。
# 用途：选常用药（preset 权威数据）+ AI 失败/未配置/超时时降级（mock），保证演示不中断。

import random

# GET /health
MOCK_HEALTH = {"status": "ok"}

# ---------- 预置常用药（离线可用，source=preset；降级时也复用，source=mock） ----------
# 数据唯一权威：shared/mock.md 第 1 节 8 种药（id/药名/三行/note/warning 逐字一致，D 维护）。
# id 与素材药盒图 assets/images/box_<id>.jpg 一一对应。
MOCK_MEDICATIONS = [
    {"id": "amoxi", "name": "阿莫西林胶囊"},
    {"id": "cefix", "name": "头孢克肟分散片"},
    {"id": "metfor", "name": "二甲双胍缓释片"},
    {"id": "ibu", "name": "布洛芬缓释胶囊"},
    {"id": "nife", "name": "硝苯地平控释片"},
    {"id": "gankang", "name": "感冒灵颗粒"},
    {"id": "statin", "name": "阿托伐他汀钙片"},
    {"id": "amlo", "name": "氨氯地平片"},
]


def _speak(name: str, dose: str, freq: str, timing: str, warning: str | None) -> str:
    """与 shared/mock.md 第 3 节 TTS 拼接规范一致：药名。dose。freq。timing。+（warning）+ 遵医嘱提醒。"""
    parts = [f"{name}。", f"{dose}。", f"{freq}。", f"{timing}。"]
    if warning:
        parts.append(f"注意：{warning}。")
    parts.append("具体请遵医嘱。")
    return "".join(parts)


def _share(name: str, dose: str, freq: str, timing: str, extra: str | None) -> str:
    """契约格式：【用药卡】药名：一次 X 片，一天 X 次，饭后吃（note/warning 有则附一句）。"""
    text = f"【用药卡】{name}：{dose}，{freq}，{timing}。"
    if extra:
        text += extra
    return text


MED_CARDS: dict[str, dict] = {
    "amoxi": {
        "drug_name": "阿莫西林胶囊",
        "per_dose": "一次 2 粒",
        "daily_times": "一天 3 次",
        "meal_timing": "饭前饭后都可以，间隔 8 小时",
        "speak_text": _speak("阿莫西林胶囊", "一次 2 粒", "一天 3 次", "饭前饭后都可以，间隔 8 小时", "青霉素过敏者禁用"),
        "share_text": _share("阿莫西林胶囊", "一次 2 粒", "一天 3 次", "饭前饭后都可以（间隔 8 小时）", "青霉素过敏者禁用。"),
        "note": None,
        "warning": "青霉素过敏者禁用",
    },
    "cefix": {
        "drug_name": "头孢克肟分散片",
        "per_dose": "一次 2 片",
        "daily_times": "一天 2 次",
        "meal_timing": "饭后吃",
        "speak_text": _speak("头孢克肟分散片", "一次 2 片", "一天 2 次", "饭后吃", "服药期间和停药 7 天内，一口酒都不能沾"),
        "share_text": _share("头孢克肟分散片", "一次 2 片", "一天 2 次", "饭后吃", "服药期间和停药 7 天内，一口酒都不能沾。"),
        "note": None,
        "warning": "服药期间和停药 7 天内，一口酒都不能沾",
    },
    "metfor": {
        "drug_name": "二甲双胍缓释片",
        "per_dose": "一次 1 片",
        "daily_times": "一天 2 次",
        "meal_timing": "随餐或饭后马上吃",
        "speak_text": _speak("二甲双胍缓释片", "一次 1 片", "一天 2 次", "随餐或饭后马上吃", None),
        "share_text": _share("二甲双胍缓释片", "一次 1 片", "一天 2 次", "随餐或饭后马上吃", "空腹吃容易拉肚子。"),
        "note": "空腹吃容易拉肚子",
        "warning": None,
    },
    "ibu": {
        "drug_name": "布洛芬缓释胶囊",
        "per_dose": "一次 1 粒",
        "daily_times": "一天 2 次",
        "meal_timing": "饭后吃",
        "speak_text": _speak("布洛芬缓释胶囊", "一次 1 粒", "一天 2 次", "饭后吃", "有胃病、哮喘请先问医生"),
        "share_text": _share("布洛芬缓释胶囊", "一次 1 粒", "一天 2 次", "饭后吃", "空腹吃伤胃；有胃病、哮喘请先问医生。"),
        "note": "空腹吃伤胃",
        "warning": "有胃病、哮喘请先问医生",
    },
    "nife": {
        "drug_name": "硝苯地平控释片",
        "per_dose": "一次 1 片",
        "daily_times": "一天 1 次",
        "meal_timing": "早晨固定时间，整片吞不能掰",
        "speak_text": _speak("硝苯地平控释片", "一次 1 片", "一天 1 次", "早晨固定时间，整片吞不能掰", None),
        "share_text": _share("硝苯地平控释片", "一次 1 片", "一天 1 次", "早晨固定时间整片吞服", "药片空壳随大便排出是正常的。"),
        "note": "药片空壳随大便排出是正常的",
        "warning": None,
    },
    "gankang": {
        "drug_name": "感冒灵颗粒",
        "per_dose": "一次 1 袋",
        "daily_times": "一天 3 次",
        "meal_timing": "开水冲服，饭后",
        "speak_text": _speak("感冒灵颗粒", "一次 1 袋", "一天 3 次", "开水冲服，饭后", "含对乙酰氨基酚，别和其他感冒药一起吃"),
        "share_text": _share("感冒灵颗粒", "一次 1 袋", "一天 3 次", "开水冲服，饭后", "含对乙酰氨基酚，别和其他感冒药一起吃。"),
        "note": None,
        "warning": "含对乙酰氨基酚，别和其他感冒药一起吃",
    },
    "statin": {
        "drug_name": "阿托伐他汀钙片",
        "per_dose": "一次 1 片",
        "daily_times": "一天 1 次",
        "meal_timing": "睡前吃最好",
        "speak_text": _speak("阿托伐他汀钙片", "一次 1 片", "一天 1 次", "睡前吃最好", None),
        "share_text": _share("阿托伐他汀钙片", "一次 1 片", "一天 1 次", "睡前吃", None),
        "note": None,
        "warning": None,
    },
    "amlo": {
        "drug_name": "氨氯地平片",
        "per_dose": "一次 1 片",
        "daily_times": "一天 1 次",
        "meal_timing": "固定时间，饭前饭后都行",
        "speak_text": _speak("氨氯地平片", "一次 1 片", "一天 1 次", "固定时间，饭前饭后都行", None),
        "share_text": _share("氨氯地平片", "一次 1 片", "一天 1 次", "固定时间吃", None),
        "note": None,
        "warning": None,
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
