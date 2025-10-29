# 快速开始指南

欢迎使用 MyAgent！本指南将帮助您在 5 分钟内快速上手并运行您的第一个 LLM 应用。

## 📋 目录

- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [配置设置](#配置设置)
- [第一个示例](#第一个示例)
- [常见问题](#常见问题)
- [下一步](#下一步)

## 🔧 环境要求

在开始之前，请确保您的系统满足以下要求：

- **Python**: 3.10 或更高版本
- **操作系统**: Windows, macOS, 或 Linux
- **网络**: 能够访问 OpenAI API 或其他兼容的 API 端点

### 检查 Python 版本

```bash
python --version
# 或
python3 --version
```

如果版本低于 3.10，请先升级 Python。

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/your-username/myagent.git
cd myagent
```

### 2. 安装依赖

#### 方法一：使用 pip

```bash
pip install -r requirements.txt
```

#### 方法二：使用项目配置

```bash
pip install -e .
```

#### 方法三：使用 Poetry（推荐）

```bash
# 安装 Poetry（如果尚未安装）
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install
poetry shell  # 激活虚拟环境
```

### 3. 验证安装

```bash
python -c "from src.core.engines.llm.base import LLM; print('安装成功！')"
```

## ⚙️ 配置设置

### 1. 获取 API 密钥

#### OpenAI API

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册账户并登录
3. 前往 [API Keys](https://platform.openai.com/api-keys) 页面
4. 点击 "Create new secret key" 创建新密钥
5. 复制并保存密钥（只显示一次）

#### 其他 API 提供商

- **阿里云 DashScope**: [获取 API Key](https://help.aliyun.com/zh/dashscope/)
- **百度千帆**: [获取 API Key](https://cloud.baidu.com/product/wenxinworkshop)
- **腾讯混元**: [获取 API Key](https://cloud.tencent.com/product/hunyuan)

### 2. API 密钥管理

**重要变更**: 从新版本开始，API 密钥不再从环境变量自动读取，需要在代码中显式提供。

#### 推荐方式：使用 .env 文件

在项目根目录创建 `.env` 文件：

```bash
# .env
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1  # 可选
```

然后在代码中加载：

```python
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取 API 密钥
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("请设置 OPENAI_API_KEY 环境变量")
```

#### 其他方式

```python
# 方式1：直接在代码中设置（不推荐用于生产环境）
api_key = "your-api-key-here"

# 方式2：从配置文件读取
import json
with open("config.json") as f:
    config = json.load(f)
    api_key = config["api_key"]

# 方式3：从命令行参数获取
import sys
api_key = sys.argv[1] if len(sys.argv) > 1 else None
```

## 🚀 第一个示例

### 1. 基础对话

创建文件 `my_first_chat.py`：

```python
import os
from dotenv import load_dotenv
from src.core.engines.llm.base import LLM

def main():
    # 加载环境变量
    load_dotenv()
    
    # 获取 API 密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误: 请设置 OPENAI_API_KEY 环境变量")
        print("请在项目根目录创建 .env 文件并添加:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    
    try:
        # 创建 LLM 实例（现在需要显式提供 API 密钥）
        llm = LLM(
            model="gpt-3.5-turbo",
            api_key=api_key
        )
        
        print("🤖 MyAgent 聊天机器人启动！")
        print("输入 'quit' 退出程序\n")
        
        while True:
            # 获取用户输入
            user_input = input("👤 您: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！")
                break
                
            if not user_input:
                continue
                
            try:
                # 发送消息并获取回复
                response = llm.chat(user_input)
                print(f"🤖 助手: {response}\n")
                
            except Exception as e:
                print(f"❌ 聊天错误: {e}\n")
                
    except Exception as e:
        print(f"❌ 初始化错误: {e}")
        print("请检查 API 密钥是否正确")

if __name__ == "__main__":
    main()
```

### 2. 运行示例

```bash
# 确保已创建 .env 文件并设置 API 密钥
python my_first_chat.py
```

### 3. 预期输出

```
🤖 MyAgent 聊天机器人启动！
输入 'quit' 退出程序

👤 您: 你好
🤖 助手: 你好！我是 AI 助手，很高兴为您服务。有什么可以帮助您的吗？

👤 您: 你能做什么？
🤖 助手: 我可以帮助您：
1. 回答各种问题
2. 协助写作和编辑
3. 解释复杂概念
4. 提供建议和想法
5. 进行对话交流

有什么具体需要帮助的吗？

👤 您: quit
👋 再见！
```

### 4. REST API 示例

除了 Python SDK，您还可以使用 REST API：

#### 启动服务器

```bash
# 启动 API 服务器
python src/server/run_server.py
```

#### 使用 curl 测试

```bash
# 基础聊天
curl -X POST "http://localhost:8000/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "config": {
      "model": "gpt-3.5-turbo",
      "api_key": "your-api-key-here"
    }
  }'
```

#### JavaScript 客户端示例

```javascript
class LLMClient {
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
        system_prompt: options.systemPrompt,
        keep_context: options.keepContext !== false,
        temperature: options.temperature || 0.7
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }
}

// 使用示例
const client = new LLMClient();
const config = {
  model: "gpt-3.5-turbo",
  api_key: "your-api-key-here"
};

client.chat("你好", config)
  .then(result => console.log(result.response))
  .catch(error => console.error('Error:', error));
```

## 🔧 进阶示例

### 1. 使用系统提示

```python
import os
from dotenv import load_dotenv
from src.core.engines.llm.base import LLM

# 加载环境变量
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 创建 LLM 实例
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=api_key
)

# 设置角色和行为
response = llm.chat(
    user_input="解释什么是机器学习",
    system_prompt="你是一位经验丰富的AI研究员，请用通俗易懂的语言解释技术概念。"
)

print(response)
```

### 2. 使用第三方 API

```python
import os
from dotenv import load_dotenv
from src.core.engines.llm.base import LLM

# 加载环境变量
load_dotenv()

# 使用阿里云 DashScope
dashscope_key = os.getenv("DASHSCOPE_API_KEY")  # 从环境变量获取
llm = LLM(
    model="qwen-turbo",
    api_key=dashscope_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = llm.chat("你好，请用中文回答")
print(response)
```

### 3. 管理对话上下文

```python
import os
from dotenv import load_dotenv
from src.core.engines.llm.base import LLM

# 加载环境变量并创建实例
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=api_key
)

# 开始对话
llm.chat("我叫张三，是一名程序员")
llm.chat("我正在学习 Python")

# 查看对话历史
history = llm.get_context()
print(f"对话历史: {len(history)} 条消息")

# 继续对话（模型会记住之前的信息）
response = llm.chat("我的职业是什么？")
print(response)  # 应该回答：程序员

# 清空上下文
llm.clear_context()
```

### 4. REST API 进阶用法

#### 上下文管理

```bash
# 设置上下文
curl -X POST "http://localhost:8000/llm/context" \
  -H "Content-Type: application/json" \
  -d '{
    "context": [
      {"role": "user", "content": "我叫张三"},
      {"role": "assistant", "content": "你好张三！"}
    ]
  }'

# 获取上下文
curl -X GET "http://localhost:8000/llm/context"

# 清空上下文
curl -X DELETE "http://localhost:8000/llm/context"
```

#### 带配置的聊天

```bash
curl -X POST "http://localhost:8000/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "解释量子计算",
    "config": {
      "model": "gpt-4",
      "api_key": "your-api-key-here"
    },
    "system_prompt": "你是一位物理学教授，请用简单的语言解释复杂概念",
    "temperature": 0.3,
    "keep_context": true
  }'
```

## ❓ 常见问题

### Q1: 出现 "ModuleNotFoundError" 错误

**问题**: `ModuleNotFoundError: No module named 'src'`

**解决方案**:
```python
# 在脚本开头添加路径设置
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 然后再导入模块
from src.core.engines.llm.base import LLM
```

### Q2: API 密钥错误

**问题**: `ValueError: api_key is required` 或 `AuthenticationError: Invalid API key`

**解决方案**:

#### 检查 API 密钥设置
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {'已设置' if api_key else '未设置'}")
print(f"API Key 长度: {len(api_key) if api_key else 0}")
```

#### 确保 .env 文件格式正确
```bash
# .env 文件内容（注意没有空格）
OPENAI_API_KEY=sk-your-actual-key-here
```

#### 验证 API 密钥有效性
```python
import os
from dotenv import load_dotenv
from src.core.engines.llm.base import LLM

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

try:
    llm = LLM(model="gpt-3.5-turbo", api_key=api_key)
    response = llm.chat("测试")
    print("✅ API 密钥有效")
except Exception as e:
    print(f"❌ API 密钥无效: {e}")
```

### Q3: 网络连接问题

**问题**: `ConnectionError` 或超时错误

**解决方案**:
```python
import os
from dotenv import load_dotenv
from src.core.engines.llm.base import LLM

# 使用代理
os.environ["HTTP_PROXY"] = "http://your-proxy:port"
os.environ["HTTPS_PROXY"] = "https://your-proxy:port"

# 或使用国内镜像/自定义端点
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = LLM(
    model="gpt-3.5-turbo",
    api_key=api_key,
    base_url="https://your-mirror-endpoint.com/v1"
)
```

### Q4: 模型不存在

**问题**: `Model not found` 错误

**解决方案**:
```python
# 使用正确的模型名称
available_models = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o"
]

llm = LLM(
    model="gpt-3.5-turbo",  # 使用可用的模型
    api_key=api_key
)
```

### Q5: REST API 错误

**问题**: HTTP 4xx 或 5xx 错误

**解决方案**:

#### 检查服务器状态
```bash
# 检查服务器健康状态
curl http://localhost:8000/health

# 检查 LLM 服务信息
curl http://localhost:8000/llm/info
```

#### 验证请求格式
```bash
# 正确的请求格式
curl -X POST "http://localhost:8000/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "config": {
      "model": "gpt-3.5-turbo",
      "api_key": "your-api-key-here"
    }
  }'
```

### Q6: 日志输出太多

**问题**: 控制台输出过多日志信息

**解决方案**:
```python
import logging

# 设置日志级别
logging.getLogger().setLevel(logging.WARNING)  # 只显示警告和错误

# 或者禁用特定模块的日志
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
```

### Q7: 环境变量未生效

**问题**: 设置了 .env 文件但仍然提示 API 密钥未设置

**解决方案**:

#### 检查 .env 文件位置
```python
import os
from pathlib import Path

# .env 文件应该在项目根目录
project_root = Path(__file__).parent.parent  # 根据脚本位置调整
env_file = project_root / ".env"
print(f".env 文件路径: {env_file}")
print(f".env 文件存在: {env_file.exists()}")
```

#### 手动指定 .env 文件路径
```python
from dotenv import load_dotenv
from pathlib import Path

# 指定 .env 文件路径
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
```

## 🎯 下一步

恭喜！您已经成功运行了第一个 MyAgent 应用。接下来您可以：

### 1. 深入学习

- 📖 阅读 [LLM 模块使用指南](llm-guide.md)
- 📚 查看 [API 参考文档](api-reference.md)
- 🏗️ 了解 [项目架构](architecture.md)

### 2. 探索示例

```bash
# 运行官方示例
cd examples
python llm_chat.py
```

### 3. 自定义开发

- 创建自己的聊天机器人
- 集成到现有项目中
- 开发特定领域的应用

### 4. 参与贡献

- 报告 Bug 或提出建议
- 贡献代码或文档
- 分享使用经验

## 📞 获取帮助

如果遇到问题，可以通过以下方式获取帮助：

- 📖 查看 [文档](README.md)
- 🐛 提交 [Issue](https://github.com/your-repo/myagent/issues)
- 💬 参与 [讨论](https://github.com/your-repo/myagent/discussions)
- 📧 发送邮件: support@myagent.com

---

**祝您使用愉快！** 🎉