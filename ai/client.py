# ai/client.py — OpenAI 兼容接口的异步调用（LLM / VLM / ASR）
# 硬性规则：async + 超时 + 异常处理；任何失败返回 None，由 logic/ 侧降级到 mock。

import base64
import mimetypes
from pathlib import Path

import httpx

from ai.config import get_settings
from ai.prompt_loader import load_prompt


def _guess_mime(filename: str) -> str:
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


class AIClient:
    """三个能力各一个方法，全部返回 str | None（None = 调用失败，走 mock）。"""

    async def chat(self, message: str) -> str | None:
        settings = get_settings()
        prompt = load_prompt("chat")
        if not settings.available or prompt is None:
            return None
        messages = [{"role": "system", "content": prompt}]
        messages.append({"role": "user", "content": message})
        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                resp = await client.post(
                    f"{settings.base_url.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.api_key}"},
                    json={"model": settings.model_name, "messages": messages},
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            return None

    async def describe(self, image: bytes, filename: str) -> str | None:
        settings = get_settings()
        prompt = load_prompt("describe")
        if not settings.available or prompt is None:
            return None
        b64 = base64.b64encode(image).decode("ascii")
        data_url = f"data:{_guess_mime(filename)};base64,{b64}"
        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                resp = await client.post(
                    f"{settings.base_url.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.api_key}"},
                    json={
                        "model": settings.vlm_model_name,
                        "messages": [
                            {"role": "system", "content": prompt},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "描述这张图片。"},
                                    {"type": "image_url", "image_url": {"url": data_url}},
                                ],
                            },
                        ],
                    },
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            return None

    async def transcribe(self, audio: bytes, filename: str) -> str | None:
        settings = get_settings()
        if not settings.available:
            return None
        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                resp = await client.post(
                    f"{settings.base_url.rstrip('/')}/audio/transcriptions",
                    headers={"Authorization": f"Bearer {settings.api_key}"},
                    data={"model": settings.asr_model_name},
                    files={"file": (filename, audio, _guess_mime(filename))},
                )
                resp.raise_for_status()
                return resp.json()["text"]
        except Exception:
            return None


_client: AIClient | None = None


def get_client() -> AIClient:
    global _client
    if _client is None:
        _client = AIClient()
    return _client
