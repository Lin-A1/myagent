#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.engines.ocr.base import OCR


# 创建 OCR 实例
ocr = OCR()

# 图片路径
image_path = project_root / "src/common/images/image001.png"

print(f"📷 识别图片: {image_path}")

# 1. 使用文件路径
print("1️⃣ 使用文件路径:")
results = ocr.recognize(str(image_path))
print(results)
print("-" * 30)

# 2. 转换为numpy array再传入
print("2️⃣ 使用numpy array:")
import cv2
import numpy as np
image_array = cv2.imread(str(image_path))
results_array = ocr.recognize(image_array)
print(results_array)
print("-" * 30)

# 3. 转换为base64再传入
print("3️⃣ 使用base64:")
import base64
with open(image_path, 'rb') as f:
    image_data = f.read()
base64_str = base64.b64encode(image_data).decode('utf-8')
results_base64 = ocr.recognize(base64_str)
print(results_base64)
print("-" * 30)

