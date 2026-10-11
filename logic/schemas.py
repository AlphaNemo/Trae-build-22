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


# ---------- 统一药品形状（契约第 1 节：前后端共用，与 ui/drug_data.py 同构） ----------
class MedicationItem(BaseModel):
    """GET /medications 列表项：选常用药大按钮。"""

    id: str = Field(..., description="药品 ID，供 /med-card 查询")
    name: str = Field(..., description="大字按钮显示名")


class MedicationsResponse(BaseModel):
    medications: list[MedicationItem]


class Lines(BaseModel):
    """三行大字：一次几片 / 一天几次 / 饭前还是饭后。"""

    dose: str = Field(..., description="大字第 1 行：一次几片，如「一次 2 粒」")
    freq: str = Field(..., description="大字第 2 行：一天几次，如「一天 3 次」")
    timing: str = Field(..., description="大字第 3 行：饭前还是饭后，如「饭后吃」")


class DrugCard(BaseModel):
    """统一药品卡：logic/mock_data.py 与 ui/drug_data.py 的数据均为此形状。

    note/warning 允许为 null；朗读文本与分享文本由前端按 lines+warning 自行拼接
    （规范见 shared/mock.md 第 3 节），不在数据里冗余存储。
    """

    id: str = Field(..., description="药品 ID，与素材图 assets/images/box_<id>.jpg 对应")
    name: str = Field(..., description="药品名")
    lines: Lines
    note: str | None = Field(None, description="生活提示（如「空腹吃伤胃」），无则 null")
    warning: str | None = Field(None, description="高危警示（如「青霉素过敏者禁用」），无则 null")


class MedCardResponse(BaseModel):
    """AI 统一形状（契约第 2 节）：result=药品卡，meta 存来源/耗时/模型。"""

    result: DrugCard
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

