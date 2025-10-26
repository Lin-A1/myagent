import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.engines.llm.base import LLM

def main():
    """LLM 聊天示例"""
    llm = LLM(
        model="deepseek-v3.2-exp", 
        api_key="sk-xxxxxxxxx", 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    response = llm.chat("你好")
    print(response)

if __name__ == "__main__":
    main()
