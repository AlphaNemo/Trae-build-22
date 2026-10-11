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
    """拍照 → AI 识别 → 统一药品卡 dict；任何不确定都返回 None 走预置。

    降级策略（分层兜底）：
    1. AI 返回 None / 无有效 JSON → None（整体降级 mock）
    2. AI 返回的 drug_name 匹配不到预置药 → None（未知药不进药盒）
    3. AI 成功匹配预置药后，三行用法含「看不清」或缺项 → 用预置卡权威 lines 兜底
       （素材药盒正面通常没有用法说明，药名识别成功即视为有效）
    """
    card = await get_client().scan(image, filename)
    if not card:
        return None

    # 必须先匹配到预置药名 —— 这是唯一硬性门槛
    preset_id = _match_preset_id(card.get("drug_name") or "")
    if preset_id is None:
        return None

    # 以预置统一形状卡为底（id/name/note/warning 保持 mock.md 权威值）
    drug = dict(mock_data.MED_CARDS[preset_id])

    # 三行用法：AI 返回清晰就用 AI 的，含"看不清"或缺项就用预置兜底
    dose = (card.get("per_dose") or "").strip()
    freq = (card.get("daily_times") or "").strip()
    timing = (card.get("meal_timing") or "").strip()

    preset_lines = drug["lines"]  # 预置权威值
    final_lines = {
        "dose": dose if dose and "看不清" not in dose else preset_lines["dose"],
        "freq": freq if freq and "看不清" not in freq else preset_lines["freq"],
        "timing": timing if timing and "看不清" not in timing else preset_lines["timing"],
    }
    drug["lines"] = final_lines
    return drug
