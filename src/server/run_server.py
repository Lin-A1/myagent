#!/usr/bin/env python3
"""
MyAgent 服务器启动脚本

启动 FastAPI 服务器，提供 OCR 和 LLM API 服务
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from src.core.base.logger import get_logger

# 初始化日志
logger = get_logger(__name__)


def main():
    """启动服务器"""
    # 设置默认环境变量
    os.environ.setdefault("LOG_LEVEL", "INFO")

    # 服务器配置
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    reload = os.getenv("SERVER_RELOAD", "true").lower() == "true"
    workers = int(os.getenv("SERVER_WORKERS", "1"))

    logger.info(f"正在启动 MyAgent 服务器...")
    logger.info(f"服务器地址: http://{host}:{port}")
    logger.info(f"API 文档: http://{host}:{port}/docs")
    logger.info(f"重载模式: {reload}")

    # 启动服务器
    uvicorn.run(
        "src.server.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,  # reload 模式下只能使用单个 worker
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    main()
