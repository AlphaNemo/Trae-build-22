# logic/schemas.py — Pydantic 模型（即契约的代码化形态）
# 字段名与 shared/contract.md / shared/mock.md 逐字一致（snake_case，大小写敏感）。
# 契约定题冻结后，如字段有变，由角色 B 同步更新此处并广播。

from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------- 通用错误结构（契约第 2 节） ----------
class ErrorBody(BaseModel):
    code: str
    message: str


class ApiError(BaseModel):
    """统一错误响应：{ "error": { "code": ..., "message": ... } }"""

    error: ErrorBody


# ---------- AI 统一形状（契约第 2 节，便于替换模型） ----------
class AIInput(BaseModel):
    input: str = Field(..., description="文本或文件引用")
    options: Optional[dict[str, Any]] = Field(default=None, description="可选项")


class AIOutput(BaseModel):
    result: Any = Field(..., description="文本或结构化数据")
    meta: dict[str, Any] = Field(default_factory=dict, description="耗时/模型名等")


# ---------- 固定接口 ----------
class HealthResponse(BaseModel):
    status: str = "ok"


# ---------- POST /chat ----------
class ChatRequest(BaseModel):
    message: str = Field(..., description="用户输入的文本")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI 回复文本")


# ---------- POST /describe（multipart: file） ----------
class DescribeResponse(BaseModel):
    filename: str = Field(..., description="上传文件名")
    size: int = Field(..., description="文件字节数")
    description: str = Field(..., description="AI 对图片的描述")


# ---------- POST /transcribe（multipart: file） ----------
class TranscribeResponse(BaseModel):
    text: str = Field(..., description="语音转写出的文本")
