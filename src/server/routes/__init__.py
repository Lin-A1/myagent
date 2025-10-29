"""
路由模块初始化

导入并暴露所有路由器
"""

from .ocr import ocr_router
from .llm import llm_router

__all__ = ["ocr_router", "llm_router"]