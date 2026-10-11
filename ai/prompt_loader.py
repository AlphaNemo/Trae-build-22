# ai/prompt_loader.py — prompt 不硬编码：纯文本文件由角色 C 提供，这里只负责读取注入
# 文件位置：ai/prompts/<name>.txt

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def load_prompt(name: str) -> str | None:
    """读取 prompt 文本；文件不存在返回 None（调用方降级到 mock，不瞎编 prompt）。"""
    path = PROMPTS_DIR / f"{name}.txt"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None
