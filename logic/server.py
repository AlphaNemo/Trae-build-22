# logic/server.py — 独立后端入口（契约调试 / A 未装配时用）
# 运行：uvicorn logic.server:app --reload --port 8000

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from logic.routes import router
from logic.schemas import ApiError, ErrorBody

app = FastAPI(title="Trae-build-22 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.exception_handler(Exception)
async def unified_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """统一错误结构：{ "error": { "code": ..., "message": ... } }（契约第 2 节）"""
    payload = ApiError(error=ErrorBody(code="internal_error", message=str(exc)))
    return JSONResponse(status_code=500, content=payload.model_dump())
