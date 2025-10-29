"""
LLM 路由接口

提供大语言模型对话的 REST API 接口
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.core.base.logger import get_logger
from src.core.engines.llm.base import LLM

logger = get_logger(__name__)

# 创建路由器
llm_router = APIRouter(prefix="/llm", tags=["LLM"])


class LLMConfig(BaseModel):
    """LLM 配置模型"""

    model: str 
    api_key: str
    base_url: Optional[str] = None


class ChatRequest(BaseModel):
    """聊天请求模型"""

    message: str
    config: LLMConfig
    system_prompt: Optional[str] = None
    keep_context: bool = True
    temperature: float = 0.7


class ContextRequest(BaseModel):
    """上下文操作请求模型"""

    config: LLMConfig
    context: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    """聊天响应模型"""

    response: str
    context: List[Dict[str, str]]
    model_info: Dict[str, Any]


class ContextMessage(BaseModel):
    """上下文消息模型"""

    role: str
    content: str


class ContextResponse(BaseModel):
    """上下文响应模型"""

    context: List[Dict[str, str]]
    count: int


@llm_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    与 LLM 进行对话

    Args:
        request: 聊天请求，包含消息内容和 LLM 配置

    Returns:
        ChatResponse: 包含 LLM 响应和上下文的响应对象

    Raises:
        HTTPException: 当 LLM 引擎初始化失败或处理失败时
    """
    try:
        # 使用前端传入的配置创建 LLM 实例
        llm_instance = LLM(
            model=request.config.model,
            api_key=request.config.api_key,
            base_url=request.config.base_url,
        )

        # 发送消息并获取响应
        response = llm_instance.chat(
            user_input=request.message,
            system_prompt=request.system_prompt,
            keep_context=request.keep_context,
            temperature=request.temperature,
        )

        # 获取当前上下文
        context = llm_instance.get_context()

        # 获取模型信息
        model_info = {
            "model": request.config.model,
            "base_url": request.config.base_url,
            "temperature": request.temperature,
        }

        return ChatResponse(response=response, context=context, model_info=model_info)

    except Exception as e:
        logger.error(f"聊天处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"聊天处理失败: {str(e)}")


@llm_router.get("/context", response_model=ContextResponse)
async def get_context(
    api_key: str = Query(..., description="API 密钥"),
    model: str = Query(default="gpt-3.5-turbo", description="模型名称"),
    base_url: Optional[str] = Query(default=None, description="API 基础 URL"),
) -> ContextResponse:
    """
    获取当前对话上下文

    Args:
        api_key: API 密钥
        model: 模型名称
        base_url: API 基础 URL

    Returns:
        ContextResponse: 包含上下文信息的响应对象

    Raises:
        HTTPException: 当获取上下文失败时
    """
    try:
        # 使用传入的配置创建 LLM 实例
        llm_instance = LLM(model=model, api_key=api_key, base_url=base_url)

        context = llm_instance.get_context()

        return ContextResponse(context=context, count=len(context))

    except Exception as e:
        logger.error(f"获取上下文失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取上下文失败: {str(e)}")


@llm_router.post("/context", response_model=ContextResponse)
async def set_context(request: ContextRequest) -> ContextResponse:
    """
    设置对话上下文

    Args:
        request: 包含 LLM 配置和上下文数据的请求

    Returns:
        ContextResponse: 包含设置后上下文信息的响应对象

    Raises:
        HTTPException: 当设置上下文失败时
    """
    try:
        # 使用传入的配置创建 LLM 实例
        llm_instance = LLM(
            model=request.config.model,
            api_key=request.config.api_key,
            base_url=request.config.base_url,
        )

        if request.context:
            llm_instance.set_context(request.context)

        context = llm_instance.get_context()

        return ContextResponse(context=context, count=len(context))

    except Exception as e:
        logger.error(f"设置上下文失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"设置上下文失败: {str(e)}")


@llm_router.delete("/context")
async def clear_context(
    api_key: str = Query(..., description="API 密钥"),
    model: str = Query(default="gpt-3.5-turbo", description="模型名称"),
    base_url: Optional[str] = Query(default=None, description="API 基础 URL"),
) -> Dict[str, Any]:
    """
    清空对话上下文

    Args:
        api_key: API 密钥
        model: 模型名称
        base_url: API 基础 URL

    Returns:
        Dict[str, Any]: 操作结果

    Raises:
        HTTPException: 当清空上下文失败时
    """
    try:
        # 使用传入的配置创建 LLM 实例
        llm_instance = LLM(model=model, api_key=api_key, base_url=base_url)

        llm_instance.clear_context()

        return {"success": True, "message": "上下文已清空", "context_count": 0}

    except Exception as e:
        logger.error(f"清空上下文失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"清空上下文失败: {str(e)}")


@llm_router.delete("/context/last")
async def delete_last_qa(
    api_key: str = Query(..., description="API 密钥"),
    model: str = Query(default="gpt-3.5-turbo", description="模型名称"),
    base_url: Optional[str] = Query(default=None, description="API 基础 URL"),
) -> Dict[str, Any]:
    """
    删除最后一轮问答

    Args:
        api_key: API 密钥
        model: 模型名称
        base_url: API 基础 URL

    Returns:
        Dict[str, Any]: 操作结果

    Raises:
        HTTPException: 当删除失败时
    """
    try:
        # 使用传入的配置创建 LLM 实例
        llm_instance = LLM(model=model, api_key=api_key, base_url=base_url)

        success = llm_instance.delete_last_qa()

        if success:
            context = llm_instance.get_context()
            return {
                "success": True,
                "message": "已删除最后一轮问答",
                "context_count": len(context),
            }
        else:
            return {
                "success": False,
                "message": "没有可删除的问答记录",
                "context_count": len(llm_instance.get_context()),
            }

    except Exception as e:
        logger.error(f"删除最后一轮问答失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除最后一轮问答失败: {str(e)}")


@llm_router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    LLM 服务健康检查

    Returns:
        Dict[str, Any]: 健康状态信息
    """
    try:
        return {
            "status": "healthy",
            "service": "LLM",
            "message": "LLM 服务运行正常",
            "note": "需要前端提供 API 配置参数",
        }
    except Exception as e:
        logger.error(f"LLM 健康检查失败: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "LLM",
            "message": f"LLM 服务异常: {str(e)}",
        }


@llm_router.get("/info")
async def get_info() -> Dict[str, Any]:
    """
    获取 LLM 服务信息

    Returns:
        Dict[str, Any]: 服务信息
    """
    return {
        "name": "LLM Service",
        "version": "1.0.0",
        "description": "大语言模型对话服务",
        "supported_models": [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-4o-mini",
        ],
        "configuration": {
            "requires_api_key": True,
            "supports_custom_base_url": True,
            "supports_temperature": True,
            "supports_context": True,
        },
        "endpoints": {
            "chat": "/llm/chat",
            "context": "/llm/context",
            "health": "/llm/health",
            "info": "/llm/info",
        },
        "timestamp": datetime.now().isoformat(),
    }
