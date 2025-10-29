import base64
import io
import logging
from typing import Any, List

import numpy as np
import paddleocr
import uvicorn
from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("./logs/paddleocr_server.log")
    ]
)
logger = logging.getLogger(__name__)

# 全局 OCR 实例
logger.info("初始化 PaddleOCR...")
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch")
logger.info("PaddleOCR 初始化完成")

app = FastAPI()


class OCRRequest(BaseModel):
    image: str


def base64_to_image(base64_str: str) -> np.ndarray:
    """Base64 转图像"""
    try:
        if base64_str.startswith("data:image"):
            base64_str = base64_str.split(",")[1]

        image_data = base64.b64decode(base64_str)
        pil_image = Image.open(io.BytesIO(image_data))

        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")

        logger.debug(f"图像转换成功，尺寸: {pil_image.size}")
        return np.array(pil_image)
    except Exception as e:
        logger.error(f"图像转换失败: {e}")
        raise


@app.post("/ocr")
async def ocr_recognize(request: OCRRequest) :
    """OCR 识别接口"""
    logger.info("收到 OCR 识别请求")
    try:
        image = base64_to_image(request.image)
        logger.info("开始 OCR 识别...")
        result = ocr.predict(image)
        logger.info(
            f"OCR 识别完成"
        )
        return {'result':[res.json['res'] for res in result]}
    except Exception as e:
        logger.error(f"OCR 识别失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check() -> dict:
    """健康检查接口"""
    return {"status": "healthy"}



if __name__ == "__main__":
    logger.info("启动 PaddleOCR 服务器，端口: 8001")
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=False)
