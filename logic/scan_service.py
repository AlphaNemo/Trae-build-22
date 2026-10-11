# logic/scan_service.py — 拍照识别服务：AI 原始输出 → 统一药品形状
# 供 logic/routes.py（POST /scan）与 ui/pages.py（进程内直调）共用。
# 规则（宁可不答，不能答错）：
#   1. AI 调用失败 / JSON 解析失败 → None（调用方回退预置演示流程）
#   2. 三行里出现「看不清」或为空 → None（真实照片拍不清用法时，不做假卡）
#   3. 药名无法匹配 8 种预置药 → None（药盒/分享按预置 id 工作，未知药不进药盒）
#   4. 匹配成功 → 以预置卡为底（id/name/note/warning 保持 mock.md 权威值），
#      仅用 AI 读到的三行覆盖 lines（这是真 AI 识别的演示价值所在）

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


async def scan_drug(image: bytes, filename: str) -> dict | None:
    """拍照 → AI 识别 → 统一药品卡 dict；任何不确定都返回 None 走预置。"""
    card = await get_client().scan(image, filename)
    if not card:
        return None

    dose = (card.get("per_dose") or "").strip()
    freq = (card.get("daily_times") or "").strip()
    timing = (card.get("meal_timing") or "").strip()
    if not (dose and freq and timing):
        return None
    if any("看不清" in v for v in (dose, freq, timing)):
        return None

    preset_id = _match_preset_id(card.get("drug_name") or "")
    if preset_id is None:
        return None

    # 以预置统一形状卡为底（id/name/note/warning 保持 mock.md 权威值），AI 三行覆盖 lines
    drug = dict(mock_data.MED_CARDS[preset_id])
    drug["lines"] = {"dose": dose, "freq": freq, "timing": timing}
    return drug
