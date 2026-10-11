# logic/routes.py — 接口层：mock/预置先行，AI 可用时才调用，失败自动降级
# 契约依据：shared/contract.md（2026-10-11 定题草案）。赛题：药品说明书三行大字卡。

import time
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile

from ai import get_client
from logic import mock_data, scan_service
from logic.schemas import (
    ChatRequest,
    ChatResponse,
    DrugCard,
    HealthResponse,
    Lines,
    MedCardRequest,
    MedCardResponse,
    MedicationItem,
    MedicationsResponse,
    TranscribeResponse,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="健康检查")
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/medications", response_model=MedicationsResponse, summary="常用药目录（选常用药）")
async def medications() -> MedicationsResponse:
    items = mock_data.list_medications()
    return MedicationsResponse(medications=[MedicationItem(**item) for item in items])


@router.post("/med-card", response_model=MedCardResponse, summary="查用药卡（预置，离线可用）")
async def med_card(request: MedCardRequest) -> MedCardResponse:
    card = mock_data.get_med_card(request.drug_id)
    if card is None:
        raise HTTPException(status_code=404, detail=f"没有找到常用药：{request.drug_id}")
    return MedCardResponse(result=DrugCard(**card), meta={"source": "preset"})


@router.post("/scan", response_model=MedCardResponse, summary="拍说明书 → 三行用药卡（AI 失败自动降级）")
async def scan(file: UploadFile = File(...)) -> MedCardResponse:
    data = await file.read()
    started = time.perf_counter()
    meta: dict[str, Any] = {}

    # 统一形状识别（逐字段诚实）：None = AI 基础设施故障（未配置/超时/异常）→ mock 兜底
    drug_dict = None
    try:
        drug_dict = await scan_service.scan_drug(data, file.filename or "photo.jpg")
    except Exception:
        drug_dict = None

    if drug_dict:
        matched = drug_dict.pop("matched", False)
        card = DrugCard(lines=Lines(**drug_dict["lines"]), **{k: v for k, v in drug_dict.items() if k != "lines"})
        meta["source"] = "ai"
        meta["matched"] = matched
        meta["model"] = "vlm"
    else:
        card = DrugCard(**mock_data.pick_med_card())
        meta["source"] = "mock"
    meta["elapsed_ms"] = int((time.perf_counter() - started) * 1000)
    return MedCardResponse(result=card, meta=meta)


@router.post("/chat", response_model=ChatResponse, summary="追问对话（加分项）")
async def chat(request: ChatRequest) -> ChatResponse:
    reply = None
    try:
        reply = await get_client().chat(request.message)
    except Exception:
        reply = None
    if not reply:
        reply = mock_data.pick(mock_data.MOCK_CHAT_REPLIES)
    return ChatResponse(reply=reply)


@router.post("/transcribe", response_model=TranscribeResponse, summary="语音 → 文字（加分项）")
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
