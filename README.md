# LLM Agent Platform

LLM Agent Platform 是一个基于混合架构设计的AI应用平台，结合了单体架构和微服务架构的优势，提供了可扩展、易维护的LLM应用开发框架。

## 项目结构

```
app/
├── agents/                 # Agent智能体相关功能
│   ├── __init__.py
│   └── service.py          # Agent服务实现
├── api/                    # API路由
│   ├── routes.py           # API路由配置
│   └── v1/                 # API v1版本
│       ├── agents.py       # Agent相关API
│       ├── auth.py         # 认证相关API
│       └── llm.py          # LLM相关API
├── core/                   # 核心服务
│   ├── __init__.py
│   ├── llm_service.py      # 核心LLM服务
│   ├── performance.py      # 性能优化工具
│   └── startup.py          # 应用启动和关闭处理
├── database/               # 数据库相关组件
│   ├── __init__.py
│   ├── config.py           # 数据库配置
│   ├── connection.py       # 数据库连接管理
│   ├── database.py         # 数据库管理器
│   ├── clients.py          # 数据库客户端集合
│   ├── redis_client.py     # Redis客户端
│   ├── minio_client.py     # MinIO客户端
│   └── milvus_client.py    # Milvus客户端
├── main.py                 # 应用入口点
├── mcp/                    # Model Coordination Protocol (MCP)
│   ├── __init__.py
│   └── protocol.py         # MCP协议实现
├── models/                 # 数据模型
└── schemas/                # Pydantic模型定义
```

## 核心组件

### 1. 数据库组件 (Database)
独立的数据库管理空间，包含：
- PostgreSQL关系型数据库支持
- Redis缓存和会话存储
- MinIO对象存储
- Milvus向量数据库

### 2. MCP协议组件 (Model Coordination Protocol)
独立的MCP协议实现空间，用于模型协调和通信。

### 3. Agent智能体组件 (Agents)
独立的Agent服务管理空间，用于创建和管理智能体。

### 4. 核心服务组件 (Core)
平台核心服务，包括LLM服务、性能优化和应用生命周期管理。

## 架构特点

1. **混合架构设计**：结合单体架构和微服务架构的优势
2. **组件隔离**：核心组件拥有独立的管理空间
3. **高可扩展性**：为未来功能扩展预留充足空间
4. **低耦合度**：模块间依赖关系清晰
5. **易维护性**：结构清晰，便于理解和维护

## 快速开始

```
# 安装依赖
pip install -r requirements.txt

# 运行应用
python run.py
```

## API文档

启动应用后，访问 `http://localhost:8000/docs` 查看API文档。

## 技术栈

- **编程语言**: Python 3.10+
- **Web框架**: FastAPI
- **虚拟环境管理**: uv
- **容器化**: Docker, Docker Compose
- **反向代理**: Nginx
- **数据库**: PostgreSQL (关系型数据)
- **缓存**: Redis (缓存和会话存储)
- **对象存储**: MinIO (文件存储)
- **向量数据库**: Milvus (向量数据存储和检索)

## 配置说明

环境变量配置在 `app/database/config.py` 中定义：

- `DATABASE_URL`: PostgreSQL数据库连接URL
- `REDIS_URL`: Redis连接URL
- `MINIO_ENDPOINT`: MinIO服务端点
- `MINIO_ACCESS_KEY`: MinIO访问密钥
- `MINIO_SECRET_KEY`: MinIO密钥
- `MILVUS_HOST`: Milvus服务主机
- `MILVUS_PORT`: Milvus服务端口
- `OPENAI_API_KEY`: OpenAI API密钥 (可选，用于实际调用OpenAI服务)
- `OPENAI_API_BASE`: OpenAI API基础URL (可选，用于实际调用OpenAI服务)

## 开发指南

### 项目结构说明

1. **app/api/**: API路由层，处理HTTP请求
2. **app/models/**: 数据模型定义
3. **app/modules/agents/**: Agent智能体相关功能
4. **app/modules/core/**: 核心业务逻辑，包括服务实现
5. **app/modules/database/**: 数据库相关组件，包括连接管理、配置和各种数据库客户端
6. **app/modules/mcp/**: MCP协议相关模块
7. **app/schemas/**: Pydantic模型，用于请求/响应验证
8. **deployments/**: 部署相关配置文件

### 添加新功能

1. 在`app/api/v1/`中创建新的路由文件
2. 在相应的模块中实现业务逻辑（`app/modules/core/`, `app/modules/database/`, `app/modules/mcp/`, `app/modules/agents/`）
3. 在`app/models/`中定义数据模型（如需要）
4. 在`app/schemas/`中定义验证模型（如需要）
5. 在`app/api/routes.py`中注册新路由

## 部署架构

系统采用多层架构设计：

1. **负载均衡层**: Nginx作为反向代理和负载均衡器
2. **应用服务层**: 多个FastAPI应用实例
3. **数据存储层**: PostgreSQL, Redis, MinIO, Milvus

## 扩展性设计

### 组件隔离

为了确保良好的可扩展性和易于维护的架构设计，系统将核心组件进行了隔离：

1. **数据库组件** (`app/modules/database/`): 包含所有数据库相关的配置、连接管理和客户端实现
2. **MCP协议模块** (`app/modules/mcp/`): 包含Model Coordination Protocol的实现
3. **Agent智能体功能** (`app/modules/agents/`): 包含Agent服务和相关功能
4. **核心业务逻辑** (`app/modules/core/`): 包含LLM服务和其他核心功能

### Agent智能体

系统为Agent智能体开发预留了完整的接口，支持：
- Agent创建和管理
- 任务分配和执行
- 状态监控和日志记录

### MCP协议扩展

系统实现了Model Coordination Protocol (MCP) 协议，支持：
- 模型发现和管理
- 统一的模型调用接口
- 跨模型协调能力

## LLM接口兼容性说明

本系统实现了与OpenAI API规范完全兼容的接口，包括：

1. **文本补全接口** (`/api/v1/llm/completions`)
   - 支持与OpenAI相同的请求参数
   - 返回与OpenAI相同的响应格式

2. **聊天补全接口** (`/api/v1/llm/chat/completions`)
   - 支持与OpenAI相同的请求参数
   - 返回与OpenAI相同的响应格式

3. **模型列表接口** (`/api/v1/llm/models`)
   - 返回与OpenAI相同的模型列表格式

开发者可以使用任何支持OpenAI API的客户端库或工具来与本系统交互，只需将API端点指向本系统即可。

## 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情