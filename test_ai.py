# test_ai.py — 验证 .env 配置与 AI 三接口（chat / scan / transcribe）能否正常调用
# 用法：在项目根目录执行  py test_ai.py
# 不依赖任何第三方绘图/音频库，测试媒体均由脚本用 stdlib 现场生成。

import asyncio
import base64
import struct
import sys
import zlib
from pathlib import Path

# 确保从项目根目录能 import ai / logic
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ai import get_client, get_settings  # noqa: E402


def _mask(key: str) -> str:
    """只显示 key 前后各 4 位，中间打码。"""
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"


def make_test_png() -> bytes:
    """生成一张 20x20 的彩色 PNG（含红/绿/蓝/白色块），用于测试 VLM 接口连通性。"""
    width, height = 20, 20
    # 每 5x5 一个色块
    pixels = []
    for y in range(height):
        for x in range(width):
            if x < 10 and y < 10:
                pixels.append((255, 0, 0))  # 红
            elif x >= 10 and y < 10:
                pixels.append((0, 255, 0))  # 绿
            elif x < 10 and y >= 10:
                pixels.append((0, 0, 255))  # 蓝
            else:
                pixels.append((255, 255, 255))  # 白
    raw = b""
    for y in range(height):
        raw += b"\x00"  # filter type 0 (None)
        for x in range(width):
            r, g, b = pixels[y * width + x]
            raw += bytes([r, g, b])

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    idat = zlib.compress(raw)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def make_test_wav() -> bytes:
    """生成 1 秒 16kHz 16-bit 单声道静音 WAV，用于测试 ASR 接口连通性。"""
    sample_rate = 16000
    num_samples = sample_rate  # 1 秒
    data = b"\x00\x00" * num_samples  # 静音
    fmt = struct.pack("<HHIIHH", 1, 1, sample_rate, sample_rate * 2, 2, 16)
    riff = struct.pack(
        "<4sI4s4sI", b"RIFF", 36 + len(data), b"WAVE", b"fmt ", 16
    )
    data_chunk = struct.pack("<4sI", b"data", len(data))
    return riff + fmt + data_chunk + data


def check_data_consistency() -> bool:
    """比对 ui/drug_data.py 与 logic/mock_data.py 的药品数据（统一药品形状逐字段）。
    shared/mock.md 为权威源：发现不一致时改代码副本，不要改 mock.md。"""
    from logic import mock_data
    from ui.drug_data import DRUGS

    problems: list[str] = []
    ui_map = {d["id"]: d for d in DRUGS}
    be_ids = [m["id"] for m in mock_data.MOCK_MEDICATIONS]

    if sorted(ui_map) != sorted(be_ids):
        problems.append(f"id 集合不一致：ui={sorted(ui_map)} backend={sorted(be_ids)}")

    for pid in sorted(set(ui_map) & set(be_ids)):
        u, card = ui_map[pid], mock_data.MED_CARDS.get(pid)
        if card is None:
            problems.append(f"[{pid}] backend 缺 MED_CARDS 卡")
            continue
        pairs = [
            ("药名", u["name"], card["name"]),
            ("一次剂量", u["lines"]["dose"], card["lines"]["dose"]),
            ("频次", u["lines"]["freq"], card["lines"]["freq"]),
            ("餐时", u["lines"]["timing"], card["lines"]["timing"]),
            ("note", u["note"], card["note"]),
            ("warning", u["warning"], card["warning"]),
        ]
        for field, uv, bv in pairs:
            if uv != bv:
                problems.append(f"[{pid}] {field} 不一致：ui={uv!r} backend={bv!r}")

    if problems:
        print("=" * 60)
        print("【数据对齐自检】发现不一致：")
        for p in problems:
            print(f"  ✗ {p}")
        print("  权威源是 shared/mock.md，请改 ui/drug_data.py 或 logic/mock_data.py。")
        print("=" * 60)
        return False

    print(f"【数据对齐自检】✅ ui/drug_data.py 与 logic/mock_data.py 完全一致（{len(ui_map)} 种药）")
    return True


async def main() -> None:
    settings = get_settings()

    print("=" * 60)
    print("【配置检查】")
    print(f"  api_key     : {_mask(settings.api_key)}")
    print(f"  base_url    : {settings.base_url}")
    print(f"  model_name  : {settings.model_name}")
    print(f"  vlm_model   : {settings.vlm_model_name}")
    print(f"  asr_model   : {settings.asr_model_name}")
    print(f"  asr_sr(Hz)  : {settings.asr_sample_rate}")
    print(f"  timeout(s)  : {settings.timeout}")
    print(f"  available   : {settings.available}")
    print("=" * 60)

    if not settings.available:
        print("  ⚠️  api_key 未配置或仍是占位符，下面的调用会直接返回 None（走 mock）。")
        print("=" * 60)

    client = get_client()

    # —— 1. chat（text → text）——
    print("\n【1/3】POST /chat  —— 文本对话")
    try:
        reply = await client.chat("你好，请用一句话介绍你自己。")
        if reply is None:
            print("  结果: None（调用失败 → 接口会降级到 mock）")
        else:
            print(f"  结果: {reply}")
    except Exception as e:
        print(f"  异常: {type(e).__name__}: {e}")

    # —— 2. scan（image → 用药卡 JSON）——
    print("\n【2/3】POST /scan —— 拍照识药（VLM → 用药卡 JSON）")
    png = make_test_png()
    try:
        card = await client.scan(png, "test.png")
        if card is None:
            print("  结果: None（调用失败或解析不出 JSON → 接口会降级到 mock）")
        else:
            print(f"  结果: {card}")
    except Exception as e:
        print(f"  异常: {type(e).__name__}: {e}")

    # —— 3. transcribe（audio → text）——
    print("\n【3/3】POST /transcribe —— 语音转文字")
    wav = make_test_wav()
    try:
        text = await client.transcribe(wav, "test.wav")
        if text is None:
            print("  结果: None（调用失败 → 接口会降级到 mock）")
            print("  提示: 若未配置 ASR 模型，此为预期行为，演示时走 mock 假数据。")
        else:
            print(f"  结果: {text}")
    except Exception as e:
        print(f"  异常: {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    print("测试完成。若 chat / scan 返回非 None，说明 .env 与多模态模型配置正确。")
    print("=" * 60)


if __name__ == "__main__":
    # py test_ai.py          → AI 三接口冒烟（chat / scan / transcribe）
    # py test_ai.py --data   → 仅做前后端药品数据对齐自检（不动 AI，秒级完成）
    if "--data" in sys.argv:
        sys.exit(0 if check_data_consistency() else 1)
    else:
        asyncio.run(main())
