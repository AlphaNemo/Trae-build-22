# logic/mock_data.py — 假数据兜底（内容与 shared/mock.md 同步，D 维护 mock.md，B 负责代码侧对齐）
# 用途：AI 未配置 / 超时 / 现场网络挂掉时，接口返回这里的假数据保证演示不中断。

import random

# GET /health
MOCK_HEALTH = {"status": "ok"}

# POST /chat —— 至少 2 条，避免演示重复穿帮（shared/mock.md 第 4 节）
MOCK_CHAT_REPLIES = [
    "药盒说明书写着：每日 3 次，饭后服用，每次 1 片。",
    "你面前是一瓶维生素 C，标签上写着每日 1 片，随餐服用。",
]

# POST /describe —— 字段与契约一致，description 要有画面感、适合语音朗读
MOCK_DESCRIPTIONS = [
    "这是一个白底蓝字的药盒，品牌名是“泰诺”，适用于头痛发热；盒子正面写着每次 1 片、每 6 小时一次，24 小时内不超过 4 次。",
    "这是一块绿色路牌，白字写着“前方 500 米 南门”，箭头指向上方，路牌固定在右侧灯柱上。",
]

# POST /transcribe
MOCK_TRANSCRIPTS = [
    "帮我看看窗外现在是什么天气。",
    "这盒药的服用说明是什么？",
]

# 异常降级文案：接口失败时由前端朗读（shared/mock.md 第 4 节）
MOCK_FALLBACK_MESSAGE = "网络有点慢，我先根据已识别的内容告诉你：这是一盒感冒药。"


def pick(options: list[str]) -> str:
    """随机取一条假数据，演示时不至于每次一样。"""
    return random.choice(options)
