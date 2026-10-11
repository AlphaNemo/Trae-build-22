# logic/routes.py — 接口层：mock 先行，AI 可用时才调用，失败自动降级 mock
# 契约依据：shared/contract.md（定题冻结后如有字段调整，B 同步改 schemas.py 与本文件）。

from fastapi import APIRouter, File, UploadFile

from ai import get_client
from logic import mock_data
from logic.schemas import ChatRequest, ChatResponse, DescribeResponse, HealthResponse, TranscribeResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="健康检查")
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/chat", response_model=ChatResponse, summary="对话（一次性返回）")
async def chat(request: ChatRequest) -> ChatResponse:
    reply = None
    try:
        reply = await get_client().chat(request.message)
    except Exception:
        reply = None
    if not reply:
        reply = mock_data.pick(mock_data.MOCK_CHAT_REPLIES)
    return ChatResponse(reply=reply)


@router.post("/describe", response_model=DescribeResponse, summary="上传图片 → AI 描述")
async def describe(file: UploadFile = File(...)) -> DescribeResponse:
    data = await file.read()
    filename = file.filename or "unknown"
    description = None
    try:
        description = await get_client().describe(data, filename)
    except Exception:
        description = None
    if not description:
        description = mock_data.pick(mock_data.MOCK_DESCRIPTIONS)
    return DescribeResponse(filename=filename, size=len(data), description=description)


@router.post("/transcribe", response_model=TranscribeResponse, summary="语音 → 文字")
async def transcribe(file: UploadFile = File(...)) -> TranscribeResponse:
    data = await file.read()
    filename = file.filename or "audio.webm"
    text = None
    try:
        text = await get_client().transcribe(data, filename)
    except Exception:
        text = None
    if not text:
        text = mock_data.pick(mock_data.MOCK_TRANSCRIPTS)
    return TranscribeResponse(text=text)
