# logic/scan_service.py — 拍照识别服务：AI 原始输出 → 统一药品形状（逐字段诚实版）
# 供 logic/routes.py（POST /scan）与 ui/pages.py（进程内直调）共用。
# 规则（宁可不答，不能答错）：
#   1. AI 调用失败 / 超时 / JSON 解析失败（基础设施故障）→ None（调用方走预置演示兜底）
#   2. AI 成功返回后**逐字段如实透出**：读清就显示，含「看不清」或缺项 → None（前端显示「无法识别」）
#   3. 药名匹配到预置药 → id/name/note/warning 用 mock.md 权威值（警示条永远可靠）
#   4. 药名匹配不到预置药 → 未验证的药品不提供用法（lines 全 None，防幻觉编造剂量）

from logic import mock_data
from ai import get_client


def _match_preset_id(drug_name: str) -> str | None:
    """AI 药名与预置药名互包含即视为同一种药（容忍「XX胶囊」「XX缓释片」等后缀差异）。"""
    name = drug_name.strip()
    if not name:
        return None
    for med in mock_data.MOCK_MEDICATIONS:
        preset = med["name"]
        if name in preset or preset in name:
            return med["id"]
    return None


def _clean_line(value: str | None) -> str | None:
    """AI 读清 → 原文；「看不清」/空白 → None（前端显示「无法识别」）。"""
    v = (value or "").strip()
    return v if v and "看不清" not in v else None


async def scan_drug(image: bytes, filename: str) -> dict | None:
    """拍照 → AI 识别 → 统一药品卡 dict（逐字段可空）。

    返回 None 仅代表基础设施故障（AI 未配置 / 超时 / 异常），调用方应走预置演示兜底。
    AI 正常应答时逐字段透出，None 字段由前端显示「无法识别」：

      - id:     匹配到预置药 → 预置 id；未匹配 → None（不可放入药盒）
      - name:   匹配 → 预置权威名；未匹配但 AI 读到名 → AI 原文；都没读到 → None
      - lines:  AI 读清的行照常显示；「看不清」/缺项 → None；
                未匹配预置药 → 三行全 None（未经验证的药品不给用法，防编造）
      - note/warning: 匹配预置 → mock.md 权威值；未匹配 → note 固定提示、warning None
      - matched: 是否命中常用药库（前端据此调整「放进药盒」等交互）
    """
    card = await get_client().scan(image, filename)
    if not card:
        return None  # 基础设施故障 → 调用方演示兜底

    # 药名与用法同样过滤：AI 回「看不清」类文本 → None（前端显示「未识别出药品」）
    ai_name = _clean_line(card.get("drug_name"))
    preset_id = _match_preset_id(ai_name or "")

    if preset_id:
        preset = dict(mock_data.MED_CARDS[preset_id])
        return {
            "id": preset_id,
            "name": preset["name"],
            "lines": {
                "dose": _clean_line(card.get("per_dose")),
                "freq": _clean_line(card.get("daily_times")),
                "timing": _clean_line(card.get("meal_timing")),
            },
            "note": preset.get("note"),
            "warning": preset.get("warning"),
            "matched": True,
        }

    # 未命中常用药库：药名可如实展示，但用法未经核实 → 全部「无法识别」
    return {
        "id": None,
        "name": ai_name,
        "lines": {"dose": None, "freq": None, "timing": None},
        "note": ("未收录在常用药库，用法仅供参考，请核对说明书原文或咨询药师"
                 if ai_name else
                 "未识别出药品信息，请拍摄说明书上印有用法用量的一页，或咨询药师"),
        "warning": None,
        "matched": False,
    }
