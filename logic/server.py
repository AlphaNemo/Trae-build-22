# logic/server.py — 独立后端入口（契约调试 / A 未装配时用）
# 运行：uvicorn logic.server:app --reload --port 8000

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from logic.routes import router
from logic.schemas import ApiError, ErrorBody

app = FastAPI(title="Trae-build-22 API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def _error(status_code: int, code: str, message: str) -> JSONResponse:
    """统一错误结构：{ "error": { "code": ..., "message": ... } }（契约第 2 节）"""
    payload = ApiError(error=ErrorBody(code=code, message=message))
    return JSONResponse(status_code=status_code, content=payload.model_dump())


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = {404: "not_found"}.get(exc.status_code, "http_error")
    return _error(exc.status_code, code, str(exc.detail))


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _error(422, "validation_error", "请求参数不符合契约，请检查字段名与类型")


@app.exception_handler(Exception)
async def unified_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return _error(500, "internal_error", str(exc))
