# 开发指南

## 环境设置

### 本地开发环境

1. 克隆项目代码库
2. 安装Python 3.10+
3. 安装uv包管理器
4. 安装项目依赖

```bash
# 安装uv
pip install uv

# 安装项目依赖
uv pip install -r requirements.txt
```

### 数据库设置

项目使用PostgreSQL作为主数据库，开发环境可以通过Docker快速启动：

```bash
# 启动PostgreSQL容器
docker run -d \
  --name postgres \
  -e POSTGRES_DB=llm_db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15
```

### 缓存设置

项目使用Redis作为缓存，开发环境可以通过Docker快速启动：

```bash
# 启动Redis容器
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 对象存储设置

项目使用MinIO作为对象存储，开发环境可以通过Docker快速启动：

```bash
# 启动MinIO容器
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /data --console-address ":9001"
```

### 向量数据库设置

项目使用Milvus作为向量数据库，开发环境可以通过Docker快速启动：

```bash
# 启动Milvus容器
docker run -d \
  --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:v2.4.9 \
  milvus run standalone
```

## 代码结构

```
app/
├── api/                 # API路由层
│   ├── v1/              # API版本1
│   │   ├── llm.py       # LLM相关API
│   │   ├── auth.py      # 认证相关API
│   │   └── agents.py    # Agent相关API
│   └── routes.py        # API路由注册
├── models/              # 数据模型
│   ├── user.py          # 用户模型
│   ├── agent.py         # Agent模型
│   └── llm.py           # LLM模型
├── modules/             # 核心功能模块
│   ├── agents/          # Agent智能体功能模块
│   │   └── agent_service.py # Agent服务
│   ├── core/            # 核心业务逻辑模块
│   │   ├── llm_service.py   # LLM服务
│   │   └── startup.py       # 启动和关闭处理
│   ├── database/        # 数据库相关组件模块
│   │   ├── config.py        # 配置管理
│   │   ├── database.py      # 数据库连接
│   │   ├── redis_client.py  # Redis客户端
│   │   ├── minio_client.py  # MinIO客户端
│   │   └── milvus_client.py # Milvus客户端
│   └── mcp/             # MCP协议相关模块
│       └── mcp_protocol.py  # MCP协议处理
├── schemas/             # 数据验证模式
└── utils/               # 工具函数
```

## 开发流程

### 添加新的API端点

1. 在`app/api/v1/`目录下创建新的API文件或修改现有文件
2. 定义请求和响应的数据模型（在`schemas/`目录下）
3. 实现业务逻辑（在相应的模块中）
4. 在`app/api/routes.py`中注册路由

### 添加新的数据模型

1. 在`app/models/`目录下创建新的模型文件
2. 继承`Base`类并定义表结构
3. 在`app/modules/database/database.py`中确保模型被正确导入

### 添加新的服务

1. 在相应的模块目录下创建新的服务文件（`app/modules/core/`, `app/modules/database/`, `app/modules/mcp/`, `app/modules/agents/`）
2. 实现服务逻辑
3. 创建全局实例以便在其他模块中使用

## LLM接口开发

### OpenAI兼容性实现

本系统实现了与OpenAI API完全兼容的接口，包括：

1. **文本补全接口** (`/api/v1/llm/completions`)
   - 支持相同的请求参数：model, prompt, temperature, max_tokens等
   - 返回相同的响应格式

2. **聊天补全接口** (`/api/v1/llm/chat/completions`)
   - 支持相同的请求参数：model, messages, temperature, max_tokens等
   - 返回相同的响应格式

3. **模型列表接口** (`/api/v1/llm/models`)
   - 返回相同的模型列表格式

### 扩展LLM服务

要扩展LLM服务以支持实际的LLM模型，可以修改`app/modules/core/llm_service.py`文件：

1. 在`__init__`方法中添加模型加载逻辑
2. 修改`create_completion`和`create_chat_completion`方法以调用实际的LLM模型
3. 确保返回格式与OpenAI API规范一致

### 集成第三方LLM

系统支持通过配置集成第三方LLM服务：

1. 设置`OPENAI_API_KEY`和`OPENAI_API_BASE`环境变量
2. 修改`llm_service.py`中的实现以调用第三方API
3. 确保请求和响应格式保持兼容

## 数据库组件开发

### 配置管理

数据库配置在`app/modules/database/config.py`中定义，包括：

- PostgreSQL连接配置
- Redis连接配置
- MinIO连接配置
- Milvus连接配置

### 数据库客户端

每个数据库都有对应的客户端实现：

1. **Redis客户端** (`app/modules/database/redis_client.py`): 提供缓存和会话存储功能
2. **MinIO客户端** (`app/modules/database/minio_client.py`): 提供对象存储功能
3. **Milvus客户端** (`app/modules/database/milvus_client.py`): 提供向量存储和检索功能

### 扩展数据库组件

要添加新的数据库支持：

1. 在`app/modules/database/`目录下创建新的客户端文件
2. 实现相应的连接和操作方法
3. 在`app/modules/database/config.py`中添加必要的配置项

## MCP协议开发

### 协议实现

MCP协议实现在`app/modules/mcp/mcp_protocol.py`中，支持：

- 模型发现和管理
- 统一的模型调用接口
- 跨模型协调能力

### 扩展MCP协议

要扩展MCP协议：

1. 修改`app/modules/mcp/mcp_protocol.py`文件
2. 添加新的方法处理逻辑
3. 确保与现有协议兼容

## Agent智能体开发

### Agent服务

Agent服务实现在`app/modules/agents/agent_service.py`中，支持：

- Agent创建和管理
- 任务分配和执行
- 状态监控和日志记录

### 扩展Agent功能

要扩展Agent功能：

1. 修改`app/modules/agents/agent_service.py`文件
2. 添加新的Agent能力
3. 更新API接口以支持新功能

## 核心业务逻辑开发

### LLM服务

LLM服务实现在`app/modules/core/llm_service.py`中，提供：

- 文本补全功能
- 聊天补全功能
- 模型管理功能

### 启动管理

启动管理实现在`app/modules/core/startup.py`中，负责：

- 应用启动时的初始化工作
- 应用关闭时的清理工作

## 测试

### 单元测试

项目使用pytest进行单元测试：

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api.py

# 运行特定测试函数
pytest tests/test_api.py::test_get_health
```

### API测试

可以使用curl或Postman等工具测试API：

```bash
# 测试健康检查端点
curl http://localhost:8000/health

# 测试LLM模型列表
curl http://localhost:8000/api/v1/llm/models

# 测试文本补全
curl -X POST http://localhost:8000/api/v1/llm/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llm-model-1",
    "prompt": "Say hello world",
    "temperature": 0.7,
    "max_tokens": 100
  }'

# 测试聊天补全
curl -X POST http://localhost:8000/api/v1/llm/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llm-model-1",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## 代码规范

### Python代码规范

项目遵循PEP 8代码规范，使用以下工具进行代码检查：

- black: 代码格式化
- flake8: 代码风格检查
- mypy: 类型检查

```bash
# 格式化代码
black .

# 检查代码风格
flake8 .

# 类型检查
mypy .
```

### Git提交规范

提交信息应遵循以下格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型包括：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 调试

### 日志查看

应用使用标准Python日志模块，可以通过以下方式查看日志：

```bash
# 查看应用日志
docker logs <container_name>

# 查看Nginx日志
tail -f deployments/nginx/logs/access.log
tail -f deployments/nginx/logs/error.log
```

### 性能监控

可以通过以下方式监控应用性能：

1. 查看系统资源使用情况
2. 检查数据库查询性能
3. 监控API响应时间

## 故障排除

### 常见问题

1. **依赖安装失败**
   - 确保已安装uv包管理器
   - 检查网络连接
   - 尝试使用国内镜像源

2. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接参数是否正确
   - 检查防火墙设置

3. **容器启动失败**
   - 检查Docker服务状态
   - 查看容器日志
   - 验证端口是否被占用

### 支持资源

- 官方文档
- GitHub Issues
- 社区论坛