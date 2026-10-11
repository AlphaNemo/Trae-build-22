# ai/__init__.py — 对外只暴露 client 与配置入口
from ai.client import get_client
from ai.config import get_settings

__all__ = ["get_client", "get_settings"]
