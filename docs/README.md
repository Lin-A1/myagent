# MyAgent

MyAgent 是一个基于 Python 的智能代理框架，专注于提供简洁、高效的 LLM（大语言模型）集成解决方案。

## 📋 目录

- [概述](#概述)
- [特性](#特性)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [文档](#文档)
- [贡献](#贡献)
- [许可证](#许可证)

## 🎯 概述

MyAgent 旨在为开发者提供一个模块化、可扩展的智能代理开发平台。当前版本实现了 LLM 引擎和 OCR 引擎模块，支持与 OpenAI 兼容的 API 进行交互，以及基于 PaddleOCR 的光学字符识别功能。

### 核心功能

- **LLM 引擎**: 支持多种大语言模型的统一接口，兼容 OpenAI API
- **OCR 引擎**: 基于 PaddleOCR 的光学字符识别，支持多种图像格式
- **REST API 服务**: 基于 FastAPI 的 HTTP 接口，支持 LLM 和 OCR 功能
- **对话管理**: 智能的上下文管理和对话历史维护
- **配置管理**: 灵活的 API 密钥和端点配置
- **日志系统**: 完整的日志记录和调试支持

## ✨ 特性

- 🚀 **简单易用**: 提供直观的 Python SDK 和 REST API 接口
- 🔧 **高度可配置**: 支持自定义模型、API 端点和配置参数
- 🌐 **多接口支持**: 同时提供 Python SDK 和 HTTP REST API
- 📝 **完整日志**: 详细的操作日志和错误追踪
- 🔄 **上下文管理**: 智能的对话上下文维护和管理
- 🛡️ **类型安全**: 完整的 Python 类型注解和数据验证
- 📚 **文档完善**: 详细的 API 文档和使用示例
- 🔌 **易于集成**: 支持多种部署方式和集成场景

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

或使用 Poetry/Rye:

```bash
pip install -e .
```

### 基本使用

```python
import os
from src.core.engines.llm.base import LLM

# 创建 LLM 实例（API Key 现在是必需参数）
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),  # 必需：从环境变量获取
    base_url="https://api.openai.com/v1"  # 可选，支持第三方 API
)

# 开始对话
response = llm.chat("你好，请介绍一下自己")
print(response)

# 继续对话（保持上下文）
response = llm.chat("请详细说明你的能力")
print(response)
```

**重要变更**: 从 v2.0 开始，`api_key` 参数是必需的，不再从环境变量自动读取。请确保在代码中显式提供 API 密钥。

更多使用示例请参考 [examples/](../examples/) 目录。

## 📁 项目结构

```
myagent/
├── src/                    # 源代码目录
│   ├── core/              # 核心模块
│   │   ├── base/          # 基础组件（日志、配置等）
│   │   └── engines/       # 引擎模块
│   │       ├── llm/       # LLM 引擎
│   │       └── ocr/       # OCR 引擎
│   ├── modules/           # 功能模块
│   │   ├── agent/         # 智能代理模块（规划中）
│   │   ├── knowledge/     # 知识库模块（规划中）
│   │   ├── mcp/           # MCP 模块（规划中）
│   │   └── rag/           # RAG 模块（规划中）
│   ├── server/            # 服务器模块
│   │   ├── main.py        # FastAPI 主应用
│   │   ├── run_server.py  # 服务器启动脚本
│   │   └── routes/        # API 路由
│   │       ├── llm.py     # LLM API 路由
│   │       └── ocr.py     # OCR API 路由
│   └── client/            # 客户端模块（规划中）
├── examples/              # 使用示例
│   ├── llm_chat.py        # LLM 对话示例
│   └── ocr_demo.py        # OCR 识别示例
├── docs/                  # 文档目录
│   ├── README.md          # 项目说明
│   ├── quick-start.md     # 快速开始指南
│   ├── llm-guide.md       # LLM 使用指南
│   ├── ocr-guide.md       # OCR 使用指南
│   ├── api-reference.md   # API 参考文档
│   ├── backend-api.md     # 后端 API 文档
│   └── architecture.md    # 架构说明
├── conf/                  # 配置文件
└── tests/                 # 测试文件（规划中）
```

## 📖 文档

### 用户指南
- [快速开始指南](quick-start.md) - 快速上手 MyAgent
- [LLM 模块使用指南](llm-guide.md) - Python SDK 使用详解
- [OCR 模块使用指南](ocr-guide.md) - 光学字符识别功能

### API 文档
- [API 参考文档](api-reference.md) - Python SDK API 完整参考
- [后端 API 文档](backend-api.md) - REST API 接口说明

### 架构文档
- [项目架构说明](architecture.md) - 系统设计和架构概览

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 使用 Ruff 进行代码格式化和检查
- 添加完整的类型注解
- 编写详细的文档字符串
- 确保测试覆盖率达到 90% 以上

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件。

## 🔗 相关链接

- [OpenAI API 文档](https://platform.openai.com/docs)
- [Python 类型注解指南](https://docs.python.org/3/library/typing.html)
- [Ruff 代码格式化工具](https://github.com/astral-sh/ruff)

---

**注意**: 本项目目前处于早期开发阶段，API 可能会发生变化。建议在生产环境使用前进行充分测试。