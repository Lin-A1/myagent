# API 参考文档

本文档提供了 MyAgent 框架所有公开 API 的详细参考信息。

## 📋 目录

- [REST API 接口](#rest-api-接口)
  - [LLM 接口](#llm-接口)
  - [OCR 接口](#ocr-接口)
- [Python SDK](#python-sdk)
  - [LLM 类](#llm-类)
  - [OCR 类](#ocr-类)
- [数据模型](#数据模型)
- [错误处理](#错误处理)
- [认证和配置](#认证和配置)

## 🌐 REST API 接口

MyAgent 提供完整的 REST API 接口，支持通过 HTTP 请求与服务进行交互。

### LLM 接口

基础路径: `/llm`

#### POST `/llm/chat` - 对话接口

与 LLM 进行对话交互。

**请求体:**
```json
{
  "message": "你好，我是用户",
  "config": {
    "model": "gpt-3.5-turbo",
    "api_key": "your-api-key",
    "base_url": "https://api.openai.com/v1"
  },
  "system_prompt": "你是一个有用的助手",
  "keep_context": true,
  "temperature": 0.7
}
```

**响应:**
```json
{
  "response": "你好！我是AI助手，很高兴为您服务。",
  "context": [
    {"role": "user", "content": "你好，我是用户"},
    {"role": "assistant", "content": "你好！我是AI助手，很高兴为您服务。"}
  ],
  "model_info": {
    "model": "gpt-3.5-turbo",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

#### GET `/llm/context` - 获取对话上下文

获取当前对话的上下文历史。

**查询参数:**
- `api_key` (必需): API 密钥
- `model` (可选): 模型名称，默认 "gpt-3.5-turbo"
- `base_url` (可选): API 基础 URL

**响应:**
```json
{
  "context": [
    {"role": "user", "content": "用户消息"},
    {"role": "assistant", "content": "助手回复"}
  ],
  "count": 2
}
```

#### POST `/llm/context` - 设置对话上下文

设置或更新对话上下文。

**请求体:**
```json
{
  "config": {
    "model": "gpt-3.5-turbo",
    "api_key": "your-api-key",
    "base_url": "https://api.openai.com/v1"
  },
  "context": [
    {"role": "user", "content": "之前的对话"},
    {"role": "assistant", "content": "之前的回复"}
  ]
}
```

#### DELETE `/llm/context` - 清空对话上下文

清空当前对话的所有上下文。

**查询参数:**
- `api_key` (必需): API 密钥
- `model` (可选): 模型名称
- `base_url` (可选): API 基础 URL

#### DELETE `/llm/context/last` - 删除最后一轮对话

删除最后一轮问答对话。

**查询参数:**
- `api_key` (必需): API 密钥
- `model` (可选): 模型名称
- `base_url` (可选): API 基础 URL

#### GET `/llm/health` - 健康检查

检查 LLM 服务的健康状态。

**响应:**
```json
{
  "status": "healthy",
  "message": "LLM service is healthy (requires frontend config)",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### GET `/llm/info` - 服务信息

获取 LLM 服务的详细信息。

**响应:**
```json
{
  "name": "MyAgent LLM Service",
  "version": "1.0.0",
  "description": "Large Language Model integration service",
  "supported_models": ["gpt-3.5-turbo", "gpt-4", "custom-models"],
  "configuration_required": {
    "api_key": "Required - Your LLM provider API key",
    "base_url": "Optional - Custom API endpoint URL",
    "temperature": "Optional - Response randomness (0.0-2.0)",
    "context": "Optional - Conversation context management"
  },
  "endpoints": ["/chat", "/context", "/health", "/info"]
}
```

### OCR 接口

基础路径: `/ocr`

详细的 OCR 接口文档请参考 [OCR 使用指南](ocr-guide.md)。

## 🐍 Python SDK

### LLM 类

`src.core.engines.llm.base.LLM`

支持上下文对话的 LLM 封装类，现在需要显式提供配置参数。

#### 构造函数

```python
def __init__(
    model: str = "gpt-3.5-turbo",
    api_key: str = None,
    base_url: str = None
) -> None
```

**参数:**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `model` | `str` | `"gpt-3.5-turbo"` | 使用的模型名称 |
| `api_key` | `str` | `None` | **必需** - LLM 提供商的 API 密钥 |
| `base_url` | `str` | `None` | 自定义 API 端点，为空时使用默认端点 |

**重要变更:**
- `api_key` 现在是必需参数，不再从环境变量自动读取
- 所有配置必须在实例化时明确提供

**示例:**

```python
from src.core.engines.llm.base import LLM

# 基本使用 (现在需要提供 API 密钥)
llm = LLM(
    model="gpt-3.5-turbo",
    api_key="your-openai-api-key"
)

# 自定义模型
llm = LLM(
    model="gpt-4",
    api_key="your-openai-api-key"
)

# 使用第三方 API
llm = LLM(
    model="qwen-turbo",
    api_key="your-api-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```

### 方法

#### `chat(user_input, system_prompt=None, keep_context=True, temperature=0.7)`

发送用户输入并返回模型回复。

**参数:**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `user_input` | `str` | 必需 | 用户本轮输入内容 |
| `system_prompt` | `Optional[str]` | `None` | 系统提示词，仅在首次对话时有效 |
| `keep_context` | `bool` | `True` | 是否将本轮对话追加到上下文中 |
| `temperature` | `float` | `0.7` | 生成温度参数，控制回复的随机性 (0.0-2.0) |

**返回值:**
- `str`: 模型的回复内容

**异常:**
- `Exception`: 当 API 调用失败时抛出异常

**行为说明:**
- 如果 `keep_context=True`，用户消息和助手回复都会被添加到对话历史中
- 如果 `keep_context=False`，本轮对话不会影响后续对话的上下文
- 如果 API 调用失败，会自动回滚已添加的用户消息
- `system_prompt` 只在对话历史为空时生效

**示例:**

```python
# 基本对话
response = llm.chat("你好")

# 带系统提示的对话
response = llm.chat(
    user_input="解释机器学习",
    system_prompt="你是一位AI专家，请用简单的语言解释复杂概念。"
)

# 不保持上下文的对话
response = llm.chat("这是一个独立的问题", keep_context=False)

# 调整创造性
creative_response = llm.chat("写一首诗", temperature=0.9)
factual_response = llm.chat("1+1等于多少", temperature=0.1)
```

#### `clear_context()`

清空当前对话上下文。

**参数:**
- 无

**返回值:**
- `None`

**示例:**

```python
# 清空对话历史
llm.clear_context()
```

#### `get_context()`

获取当前对话上下文的副本。

**参数:**
- 无

**返回值:**
- `List[Dict[str, str]]`: 对话历史的副本，每个字典包含 `role` 和 `content` 键

**示例:**

```python
# 获取对话历史
history = llm.get_context()
for message in history:
    print(f"{message['role']}: {message['content']}")
```

#### `set_context(history)`

手动设置对话上下文。

**参数:**

| 参数 | 类型 | 描述 |
|------|------|------|
| `history` | `List[Dict[str, str]]` | 要设置的对话历史记录 |

**返回值:**
- `None`

**消息格式:**
每个消息字典必须包含以下键：
- `role`: 消息角色，可选值为 `"system"`, `"user"`, `"assistant"`
- `content`: 消息内容

**示例:**

```python
# 设置自定义对话历史
custom_history = [
    {"role": "system", "content": "你是一个有用的助手"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}
]
llm.set_context(custom_history)
```

### 属性

#### `model`

**类型:** `str`  
**描述:** 当前使用的模型名称

#### `messages`

**类型:** `List[Dict[str, str]]`  
**描述:** 当前对话上下文消息列表  
**注意:** 建议使用 `get_context()` 方法获取副本，而不是直接访问此属性

#### `logger`

**类型:** `logging.Logger`  
**描述:** 日志记录器实例  
**注意:** 用于内部日志记录，通常不需要直接使用

#### `client`

**类型:** `openai.OpenAI`  
**描述:** OpenAI 客户端实例  
**注意:** 内部使用，不建议直接访问

## 🔍 OCR 类

`src.core.engines.ocr.base.OCR`

光学字符识别（OCR）客户端类，支持多种输入格式，提供简洁的文字识别接口。

### 构造函数

#### `__init__(server_url="http://localhost:8001")`

初始化 OCR 客户端实例。

**参数:**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `server_url` | `str` | `"http://localhost:8001"` | OCR 服务器地址 |

**返回值:**
- `None`

**示例:**

```python
from src.core.engines.ocr.base import OCR

# 使用默认服务器地址
ocr = OCR()

# 使用自定义服务器地址
ocr = OCR(server_url="http://192.168.1.100:8001")
```

### 方法

#### `recognize(image_input)`

识别图片中的文字内容。

**参数:**

| 参数 | 类型 | 描述 |
|------|------|------|
| `image_input` | `Union[str, np.ndarray, bytes]` | 图片输入，支持多种格式 |

**返回值:**
- `List[Any]`: OCR 识别结果列表

**异常:**
- `ValueError`: 当输入格式不支持或文件不存在时
- `requests.exceptions.RequestException`: 当网络请求失败时
- `Exception`: 其他 OCR 处理异常

**示例:**

```python
# 使用文件路径
result = ocr.recognize('/path/to/image.jpg')

# 使用 base64 字符串
result = ocr.recognize('iVBORw0KGgoAAAANSUhEUgAA...')

# 使用 numpy 数组
import cv2
image = cv2.imread('image.jpg')
result = ocr.recognize(image)

# 使用字节数据
with open('image.jpg', 'rb') as f:
    image_bytes = f.read()
result = ocr.recognize(image_bytes)
```

### 支持的输入格式

#### 1. 文件路径 (str)
```python
ocr.recognize('/home/user/document.png')
ocr.recognize('./images/receipt.jpg')
```

#### 2. Base64 字符串 (str)
```python
# 纯 base64 字符串
ocr.recognize('iVBORw0KGgoAAAANSUhEUgAA...')

# Data URL 格式
ocr.recognize('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...')
```

#### 3. NumPy 数组 (np.ndarray)
```python
import cv2
import numpy as np

# OpenCV 读取的图片
image = cv2.imread('document.jpg')
result = ocr.recognize(image)

# PIL 转换的数组
from PIL import Image
pil_image = Image.open('document.jpg')
np_array = np.array(pil_image)
result = ocr.recognize(np_array)
```

#### 4. 字节数据 (bytes)
```python
# 直接读取文件字节
with open('document.pdf', 'rb') as f:
    image_bytes = f.read()
result = ocr.recognize(image_bytes)

# 网络下载的图片
import requests
response = requests.get('https://example.com/image.jpg')
result = ocr.recognize(response.content)
```

### 日志记录

OCR 类集成了详细的日志记录功能：

```python
# 日志输出示例
2024-01-01 10:00:00 - OCR - INFO - 开始 OCR 识别，输入类型: str
2024-01-01 10:00:00 - OCR - DEBUG - 读取图片文件: /path/to/image.jpg
2024-01-01 10:00:00 - OCR - DEBUG - 成功读取图片文件，大小: 102400 字节
2024-01-01 10:00:00 - OCR - DEBUG - 图片转换为 base64 完成
2024-01-01 10:00:00 - OCR - DEBUG - 发送 OCR 请求到: http://localhost:8001/ocr
2024-01-01 10:00:01 - OCR - INFO - OCR 识别完成，识别到 5 个文本区域
```

### 错误处理

```python
try:
    result = ocr.recognize('nonexistent.jpg')
except ValueError as e:
    print(f"输入错误: {e}")
except requests.exceptions.ConnectionError:
    print("无法连接到 OCR 服务器")
except requests.exceptions.Timeout:
    print("OCR 请求超时")
except Exception as e:
    print(f"OCR 识别失败: {e}")
```

## 📝 日志系统

### 日志级别

MyAgent 使用标准的 Python 日志级别：

- `DEBUG`: 详细的调试信息
- `INFO`: 一般信息
- `WARNING`: 警告信息
- `ERROR`: 错误信息
- `CRITICAL`: 严重错误

### 日志配置

```python
import logging

# 设置日志级别
logging.getLogger().setLevel(logging.INFO)

# 查看详细调试信息
logging.getLogger().setLevel(logging.DEBUG)
```

### 日志输出示例

```
2025-10-26 02:52:34 - LLM - INFO - LLM initialized with model: gpt-3.5-turbo
2025-10-26 02:52:34 - LLM - INFO - Starting chat with user input length: 5
2025-10-26 02:52:35 - LLM - INFO - Received response from model. Reply length: 58
```

## ⚠️ 异常处理

### 常见异常类型

#### OpenAI API 异常

```python
from openai import OpenAIError, AuthenticationError, RateLimitError

try:
    response = llm.chat("你好")
except AuthenticationError:
    print("API 密钥无效")
except RateLimitError:
    print("API 调用频率超限")
except OpenAIError as e:
    print(f"OpenAI API 错误: {e}")
```

#### 网络异常

```python
import requests

try:
    response = llm.chat("你好")
except requests.exceptions.ConnectionError:
    print("网络连接失败")
except requests.exceptions.Timeout:
    print("请求超时")
```

#### 通用异常处理

```python
try:
    response = llm.chat("你好")
except Exception as e:
    print(f"发生未知错误: {e}")
    # 检查日志获取更多信息
```

## 📊 类型定义

### 消息类型

```python
from typing import Dict, List, Literal

MessageRole = Literal["system", "user", "assistant"]

Message = Dict[str, str]  # {"role": MessageRole, "content": str}

ConversationHistory = List[Message]
```

### 模型参数类型

```python
from typing import Optional

class ChatParameters:
    user_input: str
    system_prompt: Optional[str] = None
    keep_context: bool = True
    temperature: float = 0.7  # 范围: 0.0 - 2.0
```

## 🔧 配置常量

### 默认值

```python
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TOP_P = 1
DEFAULT_FREQUENCY_PENALTY = 0
DEFAULT_PRESENCE_PENALTY = 0
```

### 环境变量

| 变量名 | 描述 | 示例 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | `sk-...` |
| `OPENAI_BASE_URL` | 自定义 API 端点 | `https://api.openai.com/v1` |

## 📚 使用示例

### LLM 完整示例

```python
import os
from src.core.engines.llm.base import LLM

# 设置环境变量
os.environ["OPENAI_API_KEY"] = "your-api-key"

# 创建 LLM 实例
llm = LLM(model="gpt-3.5-turbo")

try:
    # 开始对话
    response1 = llm.chat(
        user_input="你好，我是张三",
        system_prompt="你是一个友好的助手"
    )
    print("助手:", response1)
    
    # 继续对话（保持上下文）
    response2 = llm.chat("我的名字是什么？")
    print("助手:", response2)
    
    # 查看对话历史
    history = llm.get_context()
    print(f"对话历史包含 {len(history)} 条消息")
    
    # 清空上下文
    llm.clear_context()
    
except Exception as e:
    print(f"错误: {e}")
```

### OCR 完整示例

```python
from src.core.engines.ocr.base import OCR
import cv2
import numpy as np

# 创建 OCR 实例
ocr = OCR(server_url="http://localhost:8001")

try:
    # 方式1: 使用文件路径
    result1 = ocr.recognize('/path/to/document.jpg')
    print("文件路径识别结果:", result1)
    
    # 方式2: 使用 OpenCV 读取的图片
    image = cv2.imread('/path/to/document.jpg')
    result2 = ocr.recognize(image)
    print("NumPy 数组识别结果:", result2)
    
    # 方式3: 使用 base64 字符串
    import base64
    with open('/path/to/document.jpg', 'rb') as f:
        image_data = f.read()
        b64_string = base64.b64encode(image_data).decode('utf-8')
    
    result3 = ocr.recognize(b64_string)
    print("Base64 识别结果:", result3)
    
    # 方式4: 使用字节数据
    with open('/path/to/document.jpg', 'rb') as f:
        image_bytes = f.read()
    
    result4 = ocr.recognize(image_bytes)
    print("字节数据识别结果:", result4)
    
except ValueError as e:
    print(f"输入格式错误: {e}")
except Exception as e:
    print(f"OCR 识别失败: {e}")
```

### 组合使用示例

```python
from src.core.engines.llm.base import LLM
from src.core.engines.ocr.base import OCR

# 初始化 (注意：LLM 现在需要 API 密钥)
llm = LLM(
    model="gpt-3.5-turbo",
    api_key="your-api-key"
)
ocr = OCR()

# OCR 识别文档
try:
    ocr_result = ocr.recognize('/path/to/receipt.jpg')
    
    # 提取识别到的文本
    extracted_text = ""
    for item in ocr_result:
        if isinstance(item, list) and len(item) >= 2:
            # PaddleOCR 格式: [bbox, (text, confidence)]
            text = item[1][0] if isinstance(item[1], tuple) else str(item[1])
            extracted_text += text + "\n"
    
    # 使用 LLM 分析 OCR 结果
    analysis = llm.chat(
        user_input=f"请分析这张收据的内容：\n{extracted_text}",
        system_prompt="你是一个财务助手，擅长分析收据和发票。"
    )
    
    print("OCR 识别结果:")
    print(extracted_text)
    print("\nLLM 分析结果:")
    print(analysis)
    
except Exception as e:
    print(f"处理失败: {e}")
```

## 📊 数据模型

### LLM 相关模型

#### LLMConfig
```python
class LLMConfig(BaseModel):
    model: str                    # 模型名称
    api_key: str                 # API 密钥
    base_url: Optional[str] = None  # 自定义 API 端点
```

#### ChatRequest
```python
class ChatRequest(BaseModel):
    message: str                 # 用户消息
    config: LLMConfig           # LLM 配置
    system_prompt: Optional[str] = None  # 系统提示词
    keep_context: bool = True    # 是否保持上下文
    temperature: float = 0.7     # 温度参数
```

#### ChatResponse
```python
class ChatResponse(BaseModel):
    response: str               # LLM 回复
    context: List[Dict[str, str]]  # 对话上下文
    model_info: Dict[str, Any]  # 模型信息
```

#### ContextRequest
```python
class ContextRequest(BaseModel):
    config: LLMConfig           # LLM 配置
    context: Optional[List[Dict[str, str]]] = None  # 上下文数据
```

#### ContextResponse
```python
class ContextResponse(BaseModel):
    context: List[Dict[str, str]]  # 上下文数据
    count: int                  # 消息数量
```

## ⚠️ 错误处理

### HTTP 状态码

| 状态码 | 描述 | 常见原因 |
|--------|------|----------|
| 200 | 成功 | 请求正常处理 |
| 400 | 请求错误 | 参数格式错误、缺少必需参数 |
| 401 | 认证失败 | API 密钥无效或过期 |
| 422 | 验证错误 | 请求体格式不符合要求 |
| 500 | 服务器错误 | LLM 服务异常、网络连接失败 |

### 常见错误类型

#### 1. 配置错误
```json
{
  "detail": "Invalid API key provided"
}
```

#### 2. 网络错误
```json
{
  "detail": "Failed to connect to LLM service"
}
```

#### 3. 参数验证错误
```json
{
  "detail": [
    {
      "loc": ["body", "config", "api_key"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 🔐 认证和配置

### API 密钥管理

**重要变更**: 从 v2.0 开始，所有 LLM 相关操作都需要在请求中提供 API 密钥，不再支持从环境变量自动读取。

#### REST API 认证
- **查询参数**: 在 GET/DELETE 请求中通过 `api_key` 参数提供
- **请求体**: 在 POST 请求中通过 `config.api_key` 字段提供

#### Python SDK 认证
```python
# 必须显式提供 API 密钥
llm = LLM(
    model="gpt-3.5-turbo",
    api_key="your-api-key"  # 必需参数
)
```

### 支持的 LLM 提供商

| 提供商 | 默认 base_url | 示例模型 |
|--------|---------------|----------|
| OpenAI | `https://api.openai.com/v1` | `gpt-3.5-turbo`, `gpt-4` |
| 阿里云 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-turbo`, `qwen-plus` |
| 自定义 | 用户指定 | 根据服务商而定 |

### 配置最佳实践

1. **安全性**: 不要在代码中硬编码 API 密钥
2. **环境隔离**: 为不同环境使用不同的 API 密钥
3. **错误处理**: 始终处理认证失败的情况
4. **连接超时**: 设置合理的网络超时时间

---

更多使用示例请参考 [LLM 模块使用指南](llm-guide.md) 和 [快速开始指南](quick-start.md)。