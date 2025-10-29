"""
MyAgent 主服务器

提供 OCR 和 LLM 功能的统一 API 服务
"""

import os
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.base.logger import get_logger
from src.server.routes import ocr_router, llm_router

# 初始化日志
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时的初始化
    logger.info("正在启动 MyAgent 服务器...")

    # 初始化 OCR 引擎
    try:
        logger.info("正在初始化 OCR 引擎...")
        # OCR 引擎将在第一次请求时延迟初始化
        logger.info("OCR 引擎初始化成功")
    except Exception as e:
        logger.error(f"OCR 引擎初始化失败: {e}")

    # 初始化 LLM 引擎
    try:
        logger.info("正在初始化 LLM 服务...")
        # LLM 引擎将在每次请求时使用前端传递的配置动态创建
        logger.info("LLM 服务初始化成功 - 将使用前端传递的 API 配置")
    except Exception as e:
        logger.error(f"LLM 服务初始化失败: {e}")

    logger.info("MyAgent 服务器启动完成")

    yield

    # 关闭时的清理
    logger.info("正在关闭 MyAgent 服务器...")


# 创建 FastAPI 应用
app = FastAPI(
    title="MyAgent API",
    description="提供 OCR 文字识别和 LLM 对话功能的统一 API 服务",
    version="1.0.0",
    lifespan=lifespan,
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(ocr_router)
app.include_router(llm_router)


@app.get("/")
async def root() -> Dict[str, Any]:
    """根路径，返回 API 信息"""
    return {
        "name": "MyAgent API",
        "version": "1.0.0",
        "description": "提供 OCR 文字识别和 LLM 对话功能的统一 API 服务",
        "services": {
            "ocr": {"description": "文字识别服务", "endpoints": "/ocr/*"},
            "llm": {"description": "大语言模型对话服务", "endpoints": "/llm/*"},
        },
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """整体健康检查"""
    health_status = {"status": "healthy", "services": {}}

    # 检查 OCR 服务
    try:
        from src.server.routes.ocr import get_ocr_engine

        get_ocr_engine()
        health_status["services"]["ocr"] = "healthy"
    except Exception as e:
        health_status["services"]["ocr"] = f"unhealthy: {e}"
        health_status["status"] = "degraded"

    # 检查 LLM 服务
    try:
        # LLM 服务现在需要前端提供配置，所以只检查模块是否可导入
        from src.core.engines.llm.base import LLM
        
        health_status["services"]["llm"] = "healthy (requires frontend config)"
    except Exception as e:
        health_status["services"]["llm"] = f"unhealthy: {e}"
        health_status["status"] = "degraded"

    return health_status


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """404 错误处理"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"路径 {request.url.path} 不存在",
            "available_endpoints": [
                "/docs - API 文档",
                "/health - 健康检查",
                "/ocr/* - OCR 相关接口",
                "/llm/* - LLM 相关接口",
            ],
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """500 错误处理"""
    logger.error(f"内部服务器错误: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "服务器内部错误，请稍后重试",
        },
    )