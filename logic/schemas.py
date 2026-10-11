# logic/schemas.py — Pydantic 模型（即契约的代码化形态）
# 字段名与 shared/contract.md / shared/mock.md 逐字一致（snake_case，大小写敏感）。
# 契约冻结后如字段有变，由角色 B 同步更新此处并广播。

from typing import Any

from pydantic import BaseModel, Field


# ---------- 通用错误结构（契约第 2 节） ----------
class ErrorBody(BaseModel):
    code: str
    message: str


class ApiError(BaseModel):
    """统一错误响应：{ "error": { "code": ..., "message": ... } }"""

    error: ErrorBody


# ---------- 固定接口 ----------
class HealthResponse(BaseModel):
    status: str = "ok"


# ---------- 用药卡（三行大字卡，契约第 4 节） ----------
class MedicationItem(BaseModel):
    """GET /medications 列表项：选常用药大按钮。"""

    id: str = Field(..., description="药品 ID，供 /med-card 查询")
    name: str = Field(..., description="大字按钮显示名")


class MedicationsResponse(BaseModel):
    medications: list[MedicationItem]


class MedicationCard(BaseModel):
    """三行大字卡：结果页只显示中间三行，speak/share 供两个大按钮用。"""

    drug_name: str = Field(..., description="药品名")
    per_dose: str = Field(..., description="大字第 1 行：一次几片")
    daily_times: str = Field(..., description="大字第 2 行：一天几次")
    meal_timing: str = Field(..., description="大字第 3 行：饭前还是饭后")
    speak_text: str = Field(..., description="「念给我听」完整朗读文本")
    share_text: str = Field(..., description="「发给子女」分享文本")


class MedCardResponse(BaseModel):
    """AI 统一形状（契约第 2 节）：result=用药卡，meta 存来源/耗时/模型。"""

    result: MedicationCard
    meta: dict[str, Any] = Field(default_factory=dict, description="source/model/elapsed_ms 等")


# ---------- POST /med-card ----------
class MedCardRequest(BaseModel):
    drug_id: str = Field(..., description="来自 GET /medications 的 id")


# ---------- POST /chat ----------
class ChatRequest(BaseModel):
    message: str = Field(..., description="用户追问文本")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI 回复文本")


# ---------- POST /transcribe（multipart: file） ----------
class TranscribeResponse(BaseModel):
    text: str = Field(..., description="语音转写出的文本")

