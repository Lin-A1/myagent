# LLM 模块使用指南

本指南详细介绍了 MyAgent 框架中 LLM（大语言模型）模块的 Python SDK 使用方法和最佳实践。

> 📖 **相关文档**: 如需了解后端 REST API 接口，请参考 [后端 API 文档](backend-api.md)

## 📋 目录

- [概述](#概述)
- [重要变更说明](#重要变更说明)
- [安装和导入](#安装和导入)
- [基本使用](#基本使用)
- [高级功能](#高级功能)
- [配置选项](#配置选项)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

## 🎯 概述

LLM 模块是 MyAgent 的核心组件，提供了与大语言模型交互的统一 Python SDK 接口。它支持：

- 多种 OpenAI 兼容的 API 端点（OpenAI、DashScope、自定义服务）
- 智能的对话上下文管理
- 完整的日志记录和错误处理
- 灵活的配置选项
- 同步和异步操作支持

## ⚠️ 重要变更说明

**从 v2.0 开始的重要变更:**

1. **API 密钥必需**: 所有 LLM 操作现在都需要显式提供 API 密钥，不再从环境变量自动读取
2. **无全局实例**: 移除了全局 LLM 实例，每次使用都需要创建实例并提供完整配置
3. **配置灵活性**: 支持运行时动态配置，无需预设全局配置
4. **增强错误处理**: 提供更详细的错误信息和异常类型

## 📦 安装和导入

### 环境准备

确保已安装必要的依赖：

```bash
pip install openai python-dotenv
```

### 导入模块

```python
from src.core.engines.llm.base import LLM
```

## 🚀 基本使用

### 创建 LLM 实例

**注意**: 现在必须提供 API 密钥

```python
import os
from dotenv import load_dotenv
from src.core.engines.llm.base import LLM

# 加载环境变量
load_dotenv()

# 基本配置 (OpenAI)
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 使用 GPT-4
llm = LLM(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 使用第三方 API (如阿里云)
llm = LLM(
    model="qwen-turbo",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```

### 基本对话

#### 单轮对话

```python
try:
    response = llm.chat("你好，请介绍一下自己")
    print(response)
except Exception as e:
    print(f"对话失败: {e}")
```

#### 带系统提示的对话

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

response = llm.chat(
    message="解释什么是机器学习",
    system_prompt="你是一位专业的AI研究员，请用简洁易懂的语言回答问题"
)
print(response)
```

### 使用第三方 API

#### DashScope (阿里云)

```python
llm = LLM(
    model="qwen-turbo",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = llm.chat("你好")
print(response)
```

#### 自定义 OpenAI 兼容端点

```python
llm = LLM(
    model="custom-model",
    api_key="your-custom-api-key",
    base_url="https://your-custom-endpoint.com/v1"
)

response = llm.chat("Hello")
print(response)
```



## 🔧 高级功能

### 上下文管理

#### 保持对话上下文

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 第一轮对话
response1 = llm.chat("我叫张三，今年25岁")
print(response1)

# 第二轮对话（模型会记住之前的信息）
response2 = llm.chat("我的年龄是多少？")
print(response2)  # 模型会回答：您的年龄是25岁
```

#### 不保持上下文

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 每次对话都是独立的
response1 = llm.chat("我叫张三", keep_context=False)
response2 = llm.chat("我的名字是什么？", keep_context=False)
print(response2)  # 模型不会记住之前的信息
```

#### 手动管理上下文

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 获取当前对话历史
history = llm.get_context()
print(f"当前有 {len(history)} 条消息")

# 清空对话历史
llm.clear_context()

# 设置自定义对话历史
custom_history = [
    {"role": "system", "content": "你是一个有用的助手"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}
]
llm.set_context(custom_history)
```

### 温度控制

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 更有创造性的回答（temperature 越高越随机）
creative_response = llm.chat("写一首诗", temperature=0.9)

# 更确定性的回答（temperature 越低越确定）
factual_response = llm.chat("1+1等于多少？", temperature=0.1)
```

## ⚙️ 配置选项

### Python SDK 初始化参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `model` | `str` | `"gpt-3.5-turbo"` | 使用的模型名称 |
| `api_key` | `str` | **必需** | LLM 提供商的 API 密钥 |
| `base_url` | `str` | `None` | 自定义 API 端点 |

**重要**: `api_key` 现在是必需参数，不再从环境变量自动读取。

### chat 方法参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `user_input` | `str` | 必需 | 用户输入的消息 |
| `system_prompt` | `str` | `None` | 系统提示词 |
| `keep_context` | `bool` | `True` | 是否保持对话上下文 |
| `temperature` | `float` | `0.7` | 控制回答的随机性 |



### 支持的模型

#### OpenAI 模型
- `gpt-3.5-turbo`
- `gpt-4`
- `gpt-4-turbo`
- `gpt-4o`

#### 第三方兼容模型
- 阿里云 DashScope: `qwen-turbo`, `qwen-plus`, `qwen-max`
- 其他 OpenAI 兼容的 API 端点

### 配置示例

#### Python SDK 配置
```python
# OpenAI
llm = LLM(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 阿里云 DashScope
llm = LLM(
    model="qwen-turbo",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 自定义端点
llm = LLM(
    model="custom-model",
    api_key=os.getenv("CUSTOM_API_KEY"),
    base_url="https://your-endpoint.com/v1"
)
```



## 🛡️ 错误处理

### Python SDK 错误处理

```python
try:
    llm = LLM(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    response = llm.chat("你好")
except ValueError as e:
    print(f"配置错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")
```

### 常见错误类型

| 错误类型 | 描述 | 处理建议 |
|----------|------|----------|
| `ValueError` | 配置参数错误 | 检查模型名称和API密钥格式 |
| `AuthenticationError` | 认证失败 | 检查 API 密钥是否正确 |
| `RateLimitError` | 请求频率限制 | 降低请求频率或升级账户 |
| `APIError` | API 服务错误 | 重试或联系服务提供商 |

### 网络超时处理

```python
import time

def chat_with_retry(llm, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return llm.chat(message)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"第 {attempt + 1} 次尝试失败，重试中...")
                time.sleep(2 ** attempt)  # 指数退避
            else:
                raise e

# 使用重试机制
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)
response = chat_with_retry(llm, "你好")
```

## 💡 最佳实践

### 1. 合理设置系统提示

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 好的系统提示
system_prompt = """
你是一个专业的 Python 编程助手。请遵循以下原则：
1. 提供清晰、可执行的代码示例
2. 解释代码的工作原理
3. 指出潜在的问题和最佳实践
4. 使用 Python 3.10+ 的特性
"""

response = llm.chat("如何实现单例模式？", system_prompt=system_prompt)
```

### 2. 管理对话长度

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 定期清理过长的对话历史
if len(llm.get_context()) > 20:  # 超过20条消息时清理
    # 保留最近的几条重要消息
    recent_context = llm.get_context()[-10:]
    llm.clear_context()
    llm.set_context(recent_context)
```

### 3. 使用适当的温度值

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 不同场景使用不同的温度
def get_temperature_by_task(task_type):
    temperatures = {
        "factual": 0.1,      # 事实性问题
        "creative": 0.8,     # 创意性任务
        "analysis": 0.3,     # 分析性任务
        "conversation": 0.7  # 日常对话
    }
    return temperatures.get(task_type, 0.7)

# 使用示例
temp = get_temperature_by_task("factual")
response = llm.chat("Python 的 GIL 是什么？", temperature=temp)
```

### 4. 日志监控

```python
import logging

# 启用详细日志
logging.basicConfig(level=logging.INFO)

# 监控 API 调用
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)
response = llm.chat("你好")  # 会自动记录详细的调用日志
```

## 🔍 故障排除

### 常见问题

#### 1. ModuleNotFoundError

```bash
# 确保正确设置 Python 路径
export PYTHONPATH="${PYTHONPATH}:/path/to/myagent"

# 或在代码中添加路径
import sys
sys.path.append('/path/to/myagent')
```

#### 2. API Key 错误

```python
# 检查 API Key 是否正确设置
import os
print("API Key:", os.getenv("OPENAI_API_KEY", "未设置"))

# 或直接在代码中设置
llm = LLM(
    model="gpt-3.5-turbo",
    api_key="your-actual-api-key"
)
```

#### 3. 网络连接问题

```python
# 使用代理
import os
os.environ["HTTP_PROXY"] = "http://your-proxy:port"
os.environ["HTTPS_PROXY"] = "https://your-proxy:port"

# 或使用自定义端点
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://your-proxy-endpoint.com/v1"
)
```

#### 4. 模型不存在

```python
# 检查可用模型列表
available_models = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo-preview",
    # 第三方模型
    "qwen-turbo",
    "deepseek-chat"
]

# 使用正确的模型名称
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### 调试技巧

#### 启用详细日志

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)

llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 现在会看到详细的 API 调用信息
response = llm.chat("你好")
```

#### 检查请求和响应

```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 查看对话历史
history = llm.get_context()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

## 📚 相关资源

- [OpenAI API 文档](https://platform.openai.com/docs)
- [阿里云 DashScope 文档](https://help.aliyun.com/zh/dashscope/)
- [MyAgent API 参考](api-reference.md)
- [项目架构说明](architecture.md)

---

如果遇到其他问题，请查看项目的 [Issues](https://github.com/your-repo/myagent/issues) 或提交新的问题报告。