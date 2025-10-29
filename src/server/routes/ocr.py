"""
OCR 路由接口

提供 OCR 文字识别的 REST API 接口
"""

from typing import Dict, Any, Optional
import base64
import io
from PIL import Image
import numpy as np

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from src.core.engines.ocr.base import OCR
from src.core.base.logger import get_logger

# 创建路由器
ocr_router = APIRouter(prefix="/ocr", tags=["OCR"])
logger = get_logger(__name__)

# 全局 OCR 实例
ocr_engine: Optional[OCR] = None


class OCRRequest(BaseModel):
    """OCR 请求模型"""

    image_data: str  # Base64 编码的图片数据或文件路径
    format: str = "base64"  # 数据格式: base64, file_path


class OCRResponse(BaseModel):
    """OCR 响应模型"""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


def get_ocr_engine() -> OCR:
    """获取 OCR 引擎实例"""
    global ocr_engine
    if ocr_engine is None:
        try:
            ocr_engine = OCR()
            logger.info("OCR 引擎初始化成功")
        except Exception as e:
            logger.error(f"OCR 引擎初始化失败: {e}")
            raise HTTPException(status_code=500, detail=f"OCR 引擎初始化失败: {e}")
    return ocr_engine


@ocr_router.post("/recognize", response_model=OCRResponse)
async def recognize_text(request: OCRRequest) -> OCRResponse:
    """
    文字识别接口

    支持 Base64 编码的图片数据和文件路径
    """
    try:
        ocr = get_ocr_engine()

        # 执行 OCR 识别
        result = ocr.recognize(request.image_data)

        return OCRResponse(success=True, message="识别成功", data={"result": result})

    except Exception as e:
        logger.error(f"OCR 识别失败: {e}")
        return OCRResponse(success=False, message=f"识别失败: {str(e)}")


@ocr_router.post("/recognize/upload", response_model=OCRResponse)
async def recognize_upload(file: UploadFile = File(...)) -> OCRResponse:
    """
    文件上传识别接口

    支持直接上传图片文件进行识别
    """
    try:
        # 检查文件类型
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="请上传图片文件")

        # 读取文件内容
        file_content = await file.read()

        # 转换为 Base64
        base64_data = base64.b64encode(file_content).decode("utf-8")
        image_data = f"data:{file.content_type};base64,{base64_data}"

        ocr = get_ocr_engine()
        result = ocr.recognize(image_data)

        return OCRResponse(
            success=True,
            message="识别成功",
            data={"filename": file.filename, "result": result},
        )

    except Exception as e:
        logger.error(f"文件上传识别失败: {e}")
        return OCRResponse(success=False, message=f"识别失败: {str(e)}")


@ocr_router.get("/health")
async def health_check() -> Dict[str, str]:
    """健康检查接口"""
    try:
        ocr = get_ocr_engine()
        return {"status": "healthy", "service": "OCR", "message": "OCR 服务运行正常"}
    except Exception as e:
        logger.error(f"OCR 健康检查失败: {e}")
        raise HTTPException(status_code=503, detail=f"OCR 服务不可用: {e}")


@ocr_router.get("/info")
async def get_info() -> Dict[str, Any]:
    """获取 OCR 服务信息"""
    return {
        "service": "OCR Text Recognition",
        "version": "1.0.0",
        "description": "基于 PaddleOCR 的文字识别服务",
        "supported_formats": ["image/jpeg", "image/png", "image/bmp", "image/tiff"],
        "endpoints": [
            "/ocr/recognize - POST: 文字识别",
            "/ocr/recognize/upload - POST: 文件上传识别",
            "/ocr/health - GET: 健康检查",
            "/ocr/info - GET: 服务信息",
        ],
    }