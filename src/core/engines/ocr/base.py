#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from typing import Any, List, Union
import os

import numpy as np
import requests
from PIL import Image
import io

from src.core.base.logger import get_logger


class OCR:
    """OCR 客户端"""

    def __init__(self, server_url: str = "http://localhost:8001"):
        self.server_url = server_url
        self.logger = get_logger(self.__class__.__name__)

    def _to_base64(self, image_input: Union[str, np.ndarray, bytes]) -> str:
        """将不同格式的图片输入转换为 base64"""
        if isinstance(image_input, str):
            # 检查是否为 base64 字符串
            if image_input.startswith("data:image") or self._is_base64(image_input):
                # 如果是 data URL，提取 base64 部分
                if image_input.startswith("data:image"):
                    self.logger.debug("检测到 data URL 格式输入")
                    return image_input.split(",")[1]
                self.logger.debug("检测到 base64 字符串输入")
                return image_input
            # 否则作为文件路径处理
            elif os.path.exists(image_input):
                self.logger.debug(f"读取图片文件: {image_input}")
                with open(image_input, "rb") as f:
                    image_data = f.read()
                self.logger.debug(f"成功读取图片文件，大小: {len(image_data)} 字节")
                return base64.b64encode(image_data).decode("utf-8")
            else:
                self.logger.error(f"文件路径不存在: {image_input}")
                raise ValueError(f"文件路径不存在: {image_input}")

        elif isinstance(image_input, np.ndarray):
            # numpy 数组转换
            self.logger.debug(f"转换 numpy 数组，形状: {image_input.shape}")
            pil_image = Image.fromarray(image_input)
            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            image_data = buffer.getvalue()
            self.logger.debug(f"numpy 数组转换完成，大小: {len(image_data)} 字节")
            return base64.b64encode(image_data).decode("utf-8")

        elif isinstance(image_input, bytes):
            # 字节数据直接编码
            self.logger.debug(f"编码字节数据，大小: {len(image_input)} 字节")
            return base64.b64encode(image_input).decode("utf-8")

        else:
            self.logger.error(f"不支持的图片输入类型: {type(image_input)}")
            raise ValueError(f"不支持的图片输入类型: {type(image_input)}")

    def _is_base64(self, s: str) -> bool:
        """检查字符串是否为有效的 base64"""
        try:
            base64.b64decode(s)
            return True
        except:
            return False

    def recognize(self, image_input: Union[str, np.ndarray, bytes]) -> List[Any]:
        """识别图片中的文字

        Args:
            image_input: 支持以下格式:
                - str: 文件路径 或 base64字符串 或 data URL
                - np.ndarray: numpy 图片数组
                - bytes: 图片字节数据
        """
        self.logger.info(f"开始 OCR 识别，输入类型: {type(image_input).__name__}")

        try:
            # 转换为 base64
            image_b64 = self._to_base64(image_input)
            self.logger.debug("图片转换为 base64 完成")

            # 发送请求
            self.logger.debug(f"发送 OCR 请求到: {self.server_url}/ocr")
            response = requests.post(
                f"{self.server_url}/ocr", json={"image": image_b64}
            )

            if response.status_code == 200:
                result = response.json()
                self.logger.info(
                    f"OCR 识别完成"
                )
                result = result['result'][0]
                return result
            else:
                self.logger.error(
                    f"OCR 请求失败，状态码: {response.status_code}, 响应: {response.text}"
                )
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            self.logger.error(f"网络请求异常: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"OCR 识别过程中发生异常: {str(e)}")
            raise


if __name__ == "__main__":
    # 测试
    ocr = OCR()
    result = ocr.recognize(
        "/home/lin/work/code/DeepLearning/LLM/myagent/src/common/images/image001.png"
    )
    print(result)
