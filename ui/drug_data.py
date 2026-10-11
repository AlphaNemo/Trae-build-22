"""
药品说明书 · 三行大字卡 —— 预置 8 种常见药数据
来源：PDF 方案《药品说明书 · 三行大字卡》第三节
字段严格对齐 PDF 中的 JSON 结构：
{
  "id": "amoxi",
  "name": "阿莫西林胶囊",
  "lines": { "dose": "...", "freq": "...", "timing": "..." },
  "note": "灰色小注释（可为 null）",
  "warning": "红色警示条（可为 null）"
}
"""

DRUGS = [
    {
        "id": "amoxi",
        "name": "阿莫西林胶囊",
        "lines": {
            "dose": "一次 2 粒",
            "freq": "一天 3 次",
            "timing": "饭前饭后都可以，间隔 8 小时"
        },
        "note": None,
        "warning": "青霉素过敏者禁用"
    },
    {
        "id": "cefix",
        "name": "头孢克肟分散片",
        "lines": {
            "dose": "一次 2 片",
            "freq": "一天 2 次",
            "timing": "饭后吃"
        },
        "note": None,
        "warning": "服药期间和停药 7 天内，一口酒都不能沾"
    },
    {
        "id": "metfor",
        "name": "二甲双胍缓释片",
        "lines": {
            "dose": "一次 1 片",
            "freq": "一天 2 次",
            "timing": "随餐或饭后马上吃"
        },
        "note": "空腹吃容易拉肚子",
        "warning": None
    },
    {
        "id": "ibu",
        "name": "布洛芬缓释胶囊",
        "lines": {
            "dose": "一次 1 粒",
            "freq": "一天 2 次",
            "timing": "饭后吃"
        },
        "note": "空腹吃伤胃",
        "warning": "有胃病、哮喘请先问医生"
    },
    {
        "id": "nife",
        "name": "硝苯地平控释片",
        "lines": {
            "dose": "一次 1 片",
            "freq": "一天 1 次",
            "timing": "早晨固定时间，整片吞不能掰"
        },
        "note": "药片空壳随大便排出是正常的",
        "warning": None
    },
    {
        "id": "gankang",
        "name": "感冒灵颗粒",
        "lines": {
            "dose": "一次 1 袋",
            "freq": "一天 3 次",
            "timing": "开水冲服，饭后"
        },
        "note": None,
        "warning": "含对乙酰氨基酚，别和其他感冒药一起吃"
    },
    {
        "id": "statin",
        "name": "阿托伐他汀钙片",
        "lines": {
            "dose": "一次 1 片",
            "freq": "一天 1 次",
            "timing": "睡前吃最好"
        },
        "note": None,
        "warning": None
    },
    {
        "id": "amlo",
        "name": "氨氯地平片",
        "lines": {
            "dose": "一次 1 片",
            "freq": "一天 1 次",
            "timing": "固定时间，饭前饭后都行"
        },
        "note": None,
        "warning": None
    }
]

# 方便按 id 查找
DRUG_MAP = {d["id"]: d for d in DRUGS}


def get_drug(drug_id: str) -> dict | None:
    """按 id 取药数据，找不到返回 None"""
    return DRUG_MAP.get(drug_id)
