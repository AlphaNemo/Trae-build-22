# logic/__init__.py — 对角色 A 暴露的装配入口
# A 在 main.py 中二选一：
#   1) 挂到 NiceGUI： from logic import api_router; app.include_router(api_router)
#   2) 独立起服务：  uvicorn logic.server:app --port 8000

from logic.routes import router as api_router

__all__ = ["api_router"]
