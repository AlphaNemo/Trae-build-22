# logic/bridge.py — AI 识别结果 → 前端 ui/drug_data 数据形状的适配层
# 供 ui/pages.py 拍照流程调用：recognize(图片字节, 文件名) -> drug dict | None
# 规则（宁可不答，不能答错）：
#   1. AI 调用失败 / JSON 解析失败 → None（前端回退预置演示流程）
#   2. 三行里出现「看不清」或为空 → None（真实照片拍不清用法时，不做假卡）
#   3. 药名无法匹配 8 种预置药 → None（药盒/分享按预置 id 工作，未知药不进药盒）
#   4. 匹配成功 → 以预置药为底（id/name/note/warning 保持 mock.md 权威值），
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


async def recognize(image: bytes, filename: str) -> dict | None:
    """拍照 → AI 识别 → 前端 drug dict；任何不确定都返回 None 走预置。"""
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

    # 以预置全字段卡为底（id/note/warning 保持 mock.md 权威值），AI 三行覆盖 lines
    base = mock_data.MED_CARDS[preset_id]
    drug = {"id": preset_id, "name": base["drug_name"], **base}
    drug["lines"] = {"dose": dose, "freq": freq, "timing": timing}
    return drug
