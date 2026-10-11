# ai/config.py — AI 配置：只从环境变量/.env 读取 key，绝不写死在代码里
# 变量名与 .env.example 一致；本项目不引入 python-dotenv，这里手写一个最小 .env 解析。

import os
from dataclasses import dataclass
from pathlib import Path

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def _load_env_file() -> None:
    """把 .env 里的键值写进环境变量（已存在的环境变量优先，不覆盖）。"""
    if not _ENV_PATH.is_file():
        return
    for line in _ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    model_name: str
    vlm_model_name: str
    asr_model_name: str
    asr_sample_rate: int
    dashscope_ws_url: str
    timeout: float

    @property
    def available(self) -> bool:
        """key 未填占位符即视为可用；不可用时接口直接走 mock。"""
        return bool(self.api_key) and "在这里填" not in self.api_key


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _load_env_file()
        _settings = Settings(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            model_name=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            vlm_model_name=os.environ.get("VLM_MODEL_NAME", "gpt-4o"),
            asr_model_name=os.environ.get("ASR_MODEL_NAME", "paraformer-realtime-v2"),
            asr_sample_rate=int(os.environ.get("ASR_SAMPLE_RATE", "16000")),
            # 代理/网关场景：ASR 的 WebSocket 地址（兼容旧写法 dashscope.BASE_URL）
            dashscope_ws_url=os.environ.get("DASHSCOPE_BASE_URL")
            or os.environ.get("dashscope.BASE_URL", ""),
            timeout=float(os.environ.get("AI_TIMEOUT", "20")),
        )
    return _settings
