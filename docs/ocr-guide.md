# OCR 模块使用指南

本指南详细介绍了 MyAgent 框架中 OCR（光学字符识别）模块的使用方法。

## 📋 目录

- [快速开始](#快速开始)
- [服务器部署](#服务器部署)
- [客户端使用](#客户端使用)
- [输入格式支持](#输入格式支持)
- [实际应用场景](#实际应用场景)
- [性能优化](#性能优化)
- [故障排除](#故障排除)

## 🚀 快速开始

### 1. 启动 OCR 服务器

```bash
# 进入项目目录
cd /home/lin/work/code/DeepLearning/LLM/myagent

# 启动 PaddleOCR 服务器
python src/core/engines/ocr/paddleocr/server.py
```

服务器将在 `http://localhost:8001` 启动，并提供以下端点：
- `POST /ocr` - OCR 识别接口
- `GET /health` - 健康检查接口

### 2. 使用 OCR 客户端

```python
from src.core.engines.ocr.base import OCR

# 创建 OCR 实例
ocr = OCR()

# 识别图片中的文字
result = ocr.recognize('/path/to/your/image.jpg')
print(result)
```

## 🖥️ 服务器部署

### 服务器特性

- **轻量级设计**: 基于 FastAPI，启动快速
- **PaddleOCR 引擎**: 支持中文和英文识别
- **角度分类**: 自动处理图片旋转
- **详细日志**: 完整的请求和处理日志

### 配置选项

服务器默认配置：
- 端口: `8001`
- 支持语言: 中文 (`ch`)
- 角度分类: 启用
- 日志级别: `INFO`

### 自定义配置

修改 `server.py` 中的配置：

```python
# 修改端口
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)  # 改为 8002

# 修改 OCR 配置
ocr = paddleocr.PaddleOCR(
    use_angle_cls=True,    # 角度分类
    lang="en",             # 改为英文
    use_gpu=True           # 启用 GPU（如果可用）
)
```

## 💻 客户端使用

### 基本用法

```python
from src.core.engines.ocr.base import OCR

# 初始化客户端
ocr = OCR(server_url="http://localhost:8001")

# 识别图片
result = ocr.recognize('document.jpg')
```

### 高级用法

```python
# 自定义服务器地址
ocr = OCR(server_url="http://192.168.1.100:8001")

# 批量处理
import os
image_folder = '/path/to/images'
results = {}

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        try:
            result = ocr.recognize(image_path)
            results[filename] = result
            print(f"✅ 处理完成: {filename}")
        except Exception as e:
            print(f"❌ 处理失败: {filename}, 错误: {e}")

print(f"总共处理了 {len(results)} 个文件")
```

## 📁 输入格式支持

### 1. 文件路径

```python
# 绝对路径
result = ocr.recognize('/home/user/documents/receipt.jpg')

# 相对路径
result = ocr.recognize('./images/document.png')

# 支持的格式
supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
```

### 2. Base64 字符串

```python
import base64

# 从文件生成 base64
with open('image.jpg', 'rb') as f:
    image_data = f.read()
    b64_string = base64.b64encode(image_data).decode('utf-8')

result = ocr.recognize(b64_string)

# Data URL 格式
data_url = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...'
result = ocr.recognize(data_url)
```

### 3. NumPy 数组

```python
import cv2
import numpy as np

# OpenCV 读取
image = cv2.imread('document.jpg')
result = ocr.recognize(image)

# PIL 转换
from PIL import Image
pil_image = Image.open('document.jpg')
np_array = np.array(pil_image)
result = ocr.recognize(np_array)

# 图像预处理
image = cv2.imread('noisy_document.jpg')
# 去噪
denoised = cv2.fastNlMeansDenoising(image)
# 二值化
gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
result = ocr.recognize(binary)
```

### 4. 字节数据

```python
# 直接读取文件
with open('document.pdf', 'rb') as f:
    image_bytes = f.read()
result = ocr.recognize(image_bytes)

# 网络下载
import requests
response = requests.get('https://example.com/document.jpg')
if response.status_code == 200:
    result = ocr.recognize(response.content)
```

## 🎯 实际应用场景

### 1. 发票识别与分析

```python
from src.core.engines.ocr.base import OCR
from src.core.engines.llm.base import LLM

def analyze_invoice(image_path):
    ocr = OCR()
    llm = LLM()
    
    # OCR 识别
    ocr_result = ocr.recognize(image_path)
    
    # 提取文本
    text_content = ""
    for item in ocr_result:
        if isinstance(item, list) and len(item) >= 2:
            text = item[1][0] if isinstance(item[1], tuple) else str(item[1])
            text_content += text + "\n"
    
    # LLM 分析
    analysis = llm.chat(
        user_input=f"请分析这张发票的关键信息：\n{text_content}",
        system_prompt="""你是一个财务专家，请从发票中提取以下信息：
        1. 发票号码
        2. 开票日期
        3. 销售方信息
        4. 购买方信息
        5. 商品明细
        6. 税额
        7. 总金额
        请以结构化的格式返回。"""
    )
    
    return {
        'raw_text': text_content,
        'analysis': analysis
    }

# 使用示例
result = analyze_invoice('/path/to/invoice.jpg')
print("原始文本:")
print(result['raw_text'])
print("\n分析结果:")
print(result['analysis'])
```

### 2. 证件信息提取

```python
def extract_id_info(image_path):
    ocr = OCR()
    
    # 识别证件
    result = ocr.recognize(image_path)
    
    # 提取关键信息
    extracted_info = {}
    text_lines = []
    
    for item in result:
        if isinstance(item, list) and len(item) >= 2:
            text = item[1][0] if isinstance(item[1], tuple) else str(item[1])
            text_lines.append(text)
    
    # 简单的信息提取逻辑
    for line in text_lines:
        if '姓名' in line or '名字' in line:
            extracted_info['name'] = line
        elif '身份证' in line or '证件号' in line:
            extracted_info['id_number'] = line
        elif '地址' in line or '住址' in line:
            extracted_info['address'] = line
    
    return extracted_info

# 使用示例
id_info = extract_id_info('/path/to/id_card.jpg')
print("提取的证件信息:", id_info)
```

### 3. 表格数据提取

```python
def extract_table_data(image_path):
    ocr = OCR()
    
    result = ocr.recognize(image_path)
    
    # 按位置排序文本框
    text_boxes = []
    for item in result:
        if isinstance(item, list) and len(item) >= 2:
            bbox = item[0]  # 边界框坐标
            text = item[1][0] if isinstance(item[1], tuple) else str(item[1])
            
            # 计算中心点
            center_x = sum([point[0] for point in bbox]) / 4
            center_y = sum([point[1] for point in bbox]) / 4
            
            text_boxes.append({
                'text': text,
                'x': center_x,
                'y': center_y,
                'bbox': bbox
            })
    
    # 按 Y 坐标排序（行）
    text_boxes.sort(key=lambda x: x['y'])
    
    # 简单的表格重构
    rows = []
    current_row = []
    current_y = None
    
    for box in text_boxes:
        if current_y is None or abs(box['y'] - current_y) < 20:  # 同一行
            current_row.append(box)
            current_y = box['y']
        else:  # 新行
            if current_row:
                # 按 X 坐标排序（列）
                current_row.sort(key=lambda x: x['x'])
                rows.append([box['text'] for box in current_row])
            current_row = [box]
            current_y = box['y']
    
    # 添加最后一行
    if current_row:
        current_row.sort(key=lambda x: x['x'])
        rows.append([box['text'] for box in current_row])
    
    return rows

# 使用示例
table_data = extract_table_data('/path/to/table.jpg')
for i, row in enumerate(table_data):
    print(f"第 {i+1} 行: {row}")
```

## ⚡ 性能优化

### 1. 图像预处理

```python
import cv2

def preprocess_image(image_path):
    """图像预处理以提高 OCR 准确率"""
    image = cv2.imread(image_path)
    
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 去噪
    denoised = cv2.fastNlMeansDenoising(gray)
    
    # 增强对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    # 二值化
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary

# 使用预处理后的图像
processed_image = preprocess_image('/path/to/low_quality.jpg')
result = ocr.recognize(processed_image)
```

### 2. 批量处理优化

```python
import concurrent.futures
import time

def process_single_image(image_path):
    """处理单个图像"""
    ocr = OCR()
    try:
        result = ocr.recognize(image_path)
        return {'path': image_path, 'result': result, 'status': 'success'}
    except Exception as e:
        return {'path': image_path, 'error': str(e), 'status': 'error'}

def batch_process_images(image_paths, max_workers=4):
    """批量处理图像"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_path = {
            executor.submit(process_single_image, path): path 
            for path in image_paths
        }
        
        # 收集结果
        for future in concurrent.futures.as_completed(future_to_path):
            result = future.result()
            results.append(result)
            print(f"完成: {result['path']} - {result['status']}")
    
    return results

# 使用示例
image_list = ['/path/to/img1.jpg', '/path/to/img2.jpg', '/path/to/img3.jpg']
batch_results = batch_process_images(image_list, max_workers=2)

# 统计结果
success_count = sum(1 for r in batch_results if r['status'] == 'success')
error_count = len(batch_results) - success_count
print(f"成功: {success_count}, 失败: {error_count}")
```

## 🔧 故障排除

### 常见问题

#### 1. 连接错误

```python
# 问题: requests.exceptions.ConnectionError
# 解决方案: 检查服务器是否启动

import requests

def check_server_status(server_url="http://localhost:8001"):
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ OCR 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 OCR 服务器，请检查服务器是否启动")
        return False
    except requests.exceptions.Timeout:
        print("❌ 连接超时")
        return False

# 使用前检查
if check_server_status():
    ocr = OCR()
    result = ocr.recognize('/path/to/image.jpg')
```

#### 2. 图像格式错误

```python
def validate_image(image_path):
    """验证图像文件"""
    import os
    from PIL import Image
    
    if not os.path.exists(image_path):
        raise ValueError(f"文件不存在: {image_path}")
    
    try:
        with Image.open(image_path) as img:
            img.verify()  # 验证图像完整性
        print(f"✅ 图像文件有效: {image_path}")
        return True
    except Exception as e:
        print(f"❌ 图像文件无效: {image_path}, 错误: {e}")
        return False

# 使用前验证
image_path = '/path/to/image.jpg'
if validate_image(image_path):
    result = ocr.recognize(image_path)
```

#### 3. 内存不足

```python
def process_large_image(image_path, max_size=(2048, 2048)):
    """处理大图像，自动调整尺寸"""
    from PIL import Image
    
    with Image.open(image_path) as img:
        # 检查图像尺寸
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            print(f"图像过大 {img.size}，调整到 {max_size}")
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                img.save(tmp.name, 'JPEG', quality=95)
                temp_path = tmp.name
            
            try:
                result = ocr.recognize(temp_path)
                return result
            finally:
                os.unlink(temp_path)  # 删除临时文件
        else:
            return ocr.recognize(image_path)

# 使用示例
result = process_large_image('/path/to/large_image.jpg')
```

### 日志调试

```python
import logging

# 启用详细日志
logging.getLogger().setLevel(logging.DEBUG)

# 创建 OCR 实例（会自动记录详细日志）
ocr = OCR()

# 执行识别（查看日志输出）
result = ocr.recognize('/path/to/image.jpg')
```

### 性能监控

```python
import time
import psutil

def monitor_ocr_performance(image_path):
    """监控 OCR 性能"""
    # 记录开始时间和内存
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    # 执行 OCR
    ocr = OCR()
    result = ocr.recognize(image_path)
    
    # 记录结束时间和内存
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    # 计算性能指标
    processing_time = end_time - start_time
    memory_usage = end_memory - start_memory
    
    print(f"处理时间: {processing_time:.2f} 秒")
    print(f"内存使用: {memory_usage:.2f} MB")
    print(f"识别结果数量: {len(result) if result else 0}")
    
    return result

# 使用示例
result = monitor_ocr_performance('/path/to/image.jpg')
```

---

更多信息请参考 [API 参考文档](api-reference.md) 和 [快速开始指南](quick-start.md)。