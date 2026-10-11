# ai/client.py — AI 调用统一入口
#   chat → OpenAI 兼容的 Responses API（POST /responses）
#   scan → VLM 识别药盒/说明书照片，返回用药卡 dict（解析失败返回 None，由 logic/ 降级 mock）
#   transcribe → 阿里云 DashScope SDK（Recognition，接受原始音频字节）
# 硬性规则：async + 超时 + 异常处理；任何失败返回 None，由 logic/ 侧降级到 mock。

import asyncio
import base64
import json
import mimetypes
from pathlib import Path

import httpx

from ai.config import get_settings
from ai.prompt_loader import load_prompt


def _guess_mime(filename: str) -> str:
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


def _detect_audio_format(filename: str) -> str:
    """根据文件扩展名推断 dashscope Recognition 的 format 参数。"""
    ext = Path(filename).suffix.lower().lstrip(".")
    return {
        "wav": "wav",
        "pcm": "pcm",
        "opus": "opus",
        "ogg": "opus",
        "webm": "opus",
        "mp3": "mp3",
        "amr": "amr",
        "speex": "speex",
        "m4a": "aac",
        "aac": "aac",
    }.get(ext, "wav")


def _extract_response_text(data: dict) -> str | None:
    """从 Responses API 返回中抽取 assistant 的文本。"""
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        if item.get("role") != "assistant":
            continue
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text"):
                text = content.get("text")
                if text:
                    return text
    return None


def _parse_json_object(text: str) -> dict | None:
    """从模型输出里抠出 JSON 对象（容忍 ```json 围栏和前后废话）。"""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        data = json.loads(text[start : end + 1])
    except Exception:
        return None
    return data if isinstance(data, dict) else None


class AIClient:
    """三个能力各一个方法；scan 返回 dict | None，其余返回 str | None（None = 失败，走 mock）。"""

    async def chat(self, message: str) -> str | None:
        settings = get_settings()
        prompt = load_prompt("chat")
        if not settings.available or prompt is None:
            return None
        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                resp = await client.post(
                    f"{settings.base_url.rstrip('/')}/responses",
                    headers={"Authorization": f"Bearer {settings.api_key}"},
                    json={
                        "model": settings.model_name,
                        "input": [
                            {"role": "system", "content": [{"type": "input_text", "text": prompt}]},
                            {"role": "user", "content": [{"type": "input_text", "text": message}]},
                        ],
                    },
                )
                resp.raise_for_status()
                return _extract_response_text(resp.json())
        except Exception:
            return None

    async def scan(self, image: bytes, filename: str) -> dict | None:
        """拍药盒/说明书 → 用药卡 JSON dict；任何一步失败返回 None。"""
        settings = get_settings()
        prompt = load_prompt("scan")
        if not settings.available or prompt is None:
            return None
        b64 = base64.b64encode(image).decode("ascii")
        data_url = f"data:{_guess_mime(filename)};base64,{b64}"
        try:
            async with httpx.AsyncClient(timeout=settings.timeout) as client:
                resp = await client.post(
                    f"{settings.base_url.rstrip('/')}/responses",
                    headers={"Authorization": f"Bearer {settings.api_key}"},
                    json={
                        "model": settings.vlm_model_name,
                        "input": [
                            {"role": "system", "content": [{"type": "input_text", "text": prompt}]},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "input_text", "text": "这是一张药盒或说明书的照片，请识别用药卡。"},
                                    {"type": "input_image", "image_url": data_url},
                                ],
                            },
                        ],
                    },
                )
                resp.raise_for_status()
                text = _extract_response_text(resp.json())
                if not text:
                    return None
                return _parse_json_object(text)
        except Exception:
            return None

    async def transcribe(self, audio: bytes, filename: str) -> str | None:
        settings = get_settings()
        if not settings.available:
            return None

        def _run() -> str | None:
            """同步执行 dashscope Recognition（在子线程里跑，避免阻塞事件循环）。"""
            try:
                import dashscope
                from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult

                dashscope.api_key = settings.api_key
                if settings.dashscope_ws_url:
                    dashscope.base_websocket_api_url = settings.dashscope_ws_url

                class _CB(RecognitionCallback):
                    def __init__(self) -> None:
                        self.text: str | None = None

                    def on_open(self) -> None:
                        pass

                    def on_close(self) -> None:
                        pass

                    def on_event(self, result: RecognitionResult) -> None:
                        # 每次识别结果都会回调，取最后一次的句子；兼容 Sentence 对象与 dict 两种返回
                        sentence = result.get_sentence()
                        if not sentence:
                            return
                        text = None
                        if isinstance(sentence, dict):
                            text = sentence.get("text")
                        elif hasattr(sentence, "get_text"):
                            text = sentence.get_text()
                        if text:
                            self.text = text

                    def on_complete(self) -> None:
                        pass

                    def on_error(self, result: RecognitionResult) -> None:
                        pass

                cb = _CB()
                rec = Recognition(
                    model=settings.asr_model_name,
                    callback=cb,
                    format=_detect_audio_format(filename),
                    sample_rate=settings.asr_sample_rate,
                )
                rec.start()
                rec.send_audio_frame(audio)
                rec.stop()
                return cb.text
            except Exception:
                return None

        return await asyncio.to_thread(_run)


_client: AIClient | None = None


def get_client() -> AIClient:
    global _client
    if _client is None:
        _client = AIClient()
    return _client
