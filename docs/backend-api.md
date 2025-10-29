# MyAgent 后端 API 文档

本文档详细介绍 MyAgent 后端服务的 REST API 接口。

## 📋 目录

- [服务器启动](#服务器启动)
- [API 概览](#api-概览)
- [LLM API](#llm-api)
  - [聊天接口](#聊天接口)
  - [上下文管理](#上下文管理)
  - [健康检查](#健康检查)
  - [服务信息](#服务信息)
- [OCR API](#ocr-api)
  - [文字识别](#文字识别)
- [数据模型](#数据模型)
- [错误处理](#错误处理)
- [认证配置](#认证配置)
- [客户端示例](#客户端示例)

## 🚀 服务器启动

### 启动开发服务器

```bash
# 方式1：使用 run_server.py
python src/server/run_server.py

# 方式2：使用 uvicorn
uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload
```

### 访问 API 文档

启动服务器后，可以通过以下地址访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📊 API 概览

### 基础信息

- **基础URL**: `http://localhost:8000`
- **内容类型**: `application/json`
- **字符编码**: `UTF-8`

### 端点列表

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/llm/chat` | LLM 聊天对话 |
| GET | `/llm/context/{session_id}` | 获取对话上下文 |
| POST | `/llm/context/{session_id}` | 设置对话上下文 |
| DELETE | `/llm/context/{session_id}` | 清空对话上下文 |
| DELETE | `/llm/context/{session_id}/last` | 删除最后一轮对话 |
| GET | `/llm/health` | LLM 服务健康检查 |
| GET | `/llm/info` | LLM 服务信息 |
| POST | `/ocr/recognize` | OCR 文字识别 |
| GET | `/health` | 整体服务健康检查 |

## 🤖 LLM API

### 聊天接口

**端点**: `POST /llm/chat`

发送消息给 LLM 并获取回复。

#### 请求体

```json
{
  "message": "你好，请介绍一下自己",
  "config": {
    "api_key": "your-api-key",
    "model": "gpt-3.5-turbo",
    "base_url": "https://api.openai.com/v1",
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "session_id": "user123",
  "system_prompt": "你是一个有用的AI助手",
  "keep_context": true
}
```

#### 响应

```json
{
  "response": "你好！我是一个AI助手，很高兴为您服务...",
  "session_id": "user123",
  "model": "gpt-3.5-turbo",
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 50,
    "total_tokens": 70
  }
}
```

#### cURL 示例

```bash
curl -X POST "http://localhost:8000/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "config": {
      "api_key": "your-api-key",
      "model": "gpt-3.5-turbo"
    },
    "session_id": "test_session"
  }'
```

### 上下文管理

#### 获取上下文

**端点**: `GET /llm/context/{session_id}`

```bash
curl "http://localhost:8000/llm/context/user123"
```

**响应**:
```json
{
  "session_id": "user123",
  "messages": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助您的吗？"}
  ],
  "message_count": 2
}
```

#### 设置上下文

**端点**: `POST /llm/context/{session_id}`

```bash
curl -X POST "http://localhost:8000/llm/context/user123" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "你是一个专业的翻译助手"},
      {"role": "user", "content": "请翻译：Hello World"}
    ]
  }'
```

#### 清空上下文

**端点**: `DELETE /llm/context/{session_id}`

```bash
curl -X DELETE "http://localhost:8000/llm/context/user123"
```

#### 删除最后一轮对话

**端点**: `DELETE /llm/context/{session_id}/last`

```bash
curl -X DELETE "http://localhost:8000/llm/context/user123/last"
```

### 健康检查

**端点**: `GET /llm/health`

```bash
curl "http://localhost:8000/llm/health"
```

**响应**:
```json
{
  "status": "healthy",
  "service": "llm",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 服务信息

**端点**: `GET /llm/info`

```bash
curl "http://localhost:8000/llm/info"
```

**响应**:
```json
{
  "service": "MyAgent LLM Service",
  "version": "1.0.0",
  "supported_models": [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo-preview"
  ],
  "features": [
    "chat",
    "context_management",
    "multi_model_support"
  ]
}
```

## 🔍 OCR API

### 文字识别

**端点**: `POST /ocr/recognize`

#### 请求体

支持多种输入格式：

```json
{
  "input": {
    "type": "file_path",
    "data": "/path/to/image.jpg"
  }
}
```

或者：

```json
{
  "input": {
    "type": "base64",
    "data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
  }
}
```

#### 响应

```json
{
  "text": "识别出的文字内容",
  "confidence": 0.95,
  "processing_time": 1.23
}
```

#### cURL 示例

```bash
curl -X POST "http://localhost:8000/ocr/recognize" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "type": "file_path",
      "data": "/path/to/image.jpg"
    }
  }'
```

## 📋 数据模型

### LLMConfig

```json
{
  "api_key": "string (required)",
  "model": "string (default: gpt-3.5-turbo)",
  "base_url": "string (optional)",
  "temperature": "number (0.0-2.0, default: 0.7)",
  "max_tokens": "integer (optional)",
  "timeout": "integer (default: 30)"
}
```

### ChatRequest

```json
{
  "message": "string (required)",
  "config": "LLMConfig (required)",
  "session_id": "string (optional)",
  "system_prompt": "string (optional)",
  "keep_context": "boolean (default: true)"
}
```

### ChatResponse

```json
{
  "response": "string",
  "session_id": "string",
  "model": "string",
  "usage": {
    "prompt_tokens": "integer",
    "completion_tokens": "integer",
    "total_tokens": "integer"
  }
}
```

### ContextRequest

```json
{
  "messages": [
    {
      "role": "string (user|assistant|system)",
      "content": "string"
    }
  ]
}
```

### ContextResponse

```json
{
  "session_id": "string",
  "messages": "array",
  "message_count": "integer"
}
```

## ❌ 错误处理

### HTTP 状态码

| 状态码 | 描述 | 示例场景 |
|--------|------|----------|
| 200 | 成功 | 请求处理成功 |
| 400 | 请求错误 | 参数格式错误、缺少必需参数 |
| 401 | 认证失败 | API 密钥无效或缺失 |
| 404 | 资源不存在 | 会话ID不存在 |
| 422 | 参数验证失败 | 参数类型错误 |
| 500 | 服务器内部错误 | LLM API 调用失败 |
| 503 | 服务不可用 | 外部服务暂时不可用 |

### 错误响应格式

```json
{
  "detail": {
    "error": "error_type",
    "message": "详细错误信息",
    "code": "ERROR_CODE"
  }
}
```

### 常见错误类型

#### 配置错误 (400)

```json
{
  "detail": {
    "error": "configuration_error",
    "message": "api_key is required",
    "code": "MISSING_API_KEY"
  }
}
```

#### 认证错误 (401)

```json
{
  "detail": {
    "error": "authentication_error",
    "message": "Invalid API key",
    "code": "INVALID_API_KEY"
  }
}
```

#### 模型错误 (400)

```json
{
  "detail": {
    "error": "model_error",
    "message": "Model 'invalid-model' not found",
    "code": "MODEL_NOT_FOUND"
  }
}
```

## 🔐 认证配置

### API 密钥管理

API 密钥通过请求体中的 `config.api_key` 字段传递：

```json
{
  "message": "你好",
  "config": {
    "api_key": "your-openai-api-key"
  }
}
```

### 支持的 LLM 提供商

#### OpenAI

```json
{
  "api_key": "sk-...",
  "model": "gpt-3.5-turbo",
  "base_url": "https://api.openai.com/v1"
}
```

#### DashScope (阿里云)

```json
{
  "api_key": "sk-...",
  "model": "qwen-turbo",
  "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
}
```

#### 自定义 OpenAI 兼容服务

```json
{
  "api_key": "your-api-key",
  "model": "custom-model",
  "base_url": "https://your-custom-endpoint.com/v1"
}
```

## 💻 客户端示例

### JavaScript 客户端

```javascript
class MyAgentClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async chat(message, config, options = {}) {
    const response = await fetch(`${this.baseUrl}/llm/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        config,
        ...options
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`API Error: ${error.detail.message}`);
    }

    return await response.json();
  }

  async getContext(sessionId) {
    const response = await fetch(`${this.baseUrl}/llm/context/${sessionId}`);
    return await response.json();
  }

  async clearContext(sessionId) {
    await fetch(`${this.baseUrl}/llm/context/${sessionId}`, {
      method: 'DELETE'
    });
  }
}

// 使用示例
const client = new MyAgentClient();

try {
  const result = await client.chat('你好', {
    api_key: 'your-api-key',
    model: 'gpt-3.5-turbo'
  }, {
    session_id: 'user123'
  });
  
  console.log(result.response);
} catch (error) {
  console.error('聊天失败:', error.message);
}
```

### Python 客户端

```python
import requests
import json

class MyAgentClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def chat(self, message: str, config: dict, **kwargs):
        """发送聊天消息"""
        url = f"{self.base_url}/llm/chat"
        data = {
            "message": message,
            "config": config,
            **kwargs
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_context(self, session_id: str):
        """获取对话上下文"""
        url = f"{self.base_url}/llm/context/{session_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def clear_context(self, session_id: str):
        """清空对话上下文"""
        url = f"{self.base_url}/llm/context/{session_id}"
        response = requests.delete(url)
        response.raise_for_status()

# 使用示例
client = MyAgentClient()

try:
    result = client.chat(
        message="你好",
        config={
            "api_key": "your-api-key",
            "model": "gpt-3.5-turbo"
        },
        session_id="user123"
    )
    print(result["response"])
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

### curl 脚本示例

```bash
#!/bin/bash

# 配置
BASE_URL="http://localhost:8000"
API_KEY="your-api-key"
SESSION_ID="test_session"

# 聊天函数
chat() {
    local message="$1"
    curl -s -X POST "${BASE_URL}/llm/chat" \
        -H "Content-Type: application/json" \
        -d "{
            \"message\": \"${message}\",
            \"config\": {
                \"api_key\": \"${API_KEY}\",
                \"model\": \"gpt-3.5-turbo\"
            },
            \"session_id\": \"${SESSION_ID}\"
        }" | jq -r '.response'
}

# 获取上下文
get_context() {
    curl -s "${BASE_URL}/llm/context/${SESSION_ID}" | jq '.'
}

# 清空上下文
clear_context() {
    curl -s -X DELETE "${BASE_URL}/llm/context/${SESSION_ID}"
}

# 使用示例
echo "发送消息..."
chat "你好，请介绍一下自己"

echo -e "\n获取上下文..."
get_context

echo -e "\n清空上下文..."
clear_context
```

## 🔧 部署配置

### Docker 部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "src.server.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 环境变量

```bash
# 服务配置
HOST=0.0.0.0
PORT=8000
WORKERS=4

# 日志配置
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS 配置
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

---

## 📞 技术支持

如有问题，请参考：

- [快速开始指南](quick-start.md)
- [LLM 使用指南](llm-guide.md)
- [API 参考文档](api-reference.md)
- [架构文档](architecture.md)

或提交 Issue 到项目仓库。