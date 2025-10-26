from openai import OpenAI
from typing import Optional, List, Dict, Any
import logging

from src.core.base.logger import get_logger

class LLM:
    """
    支持上下文对话的 LLM 封装类
    默认使用 OpenAI GPT 系列模型，可扩展其他后端
    
    Attributes:
        model: 模型名称
        messages: 对话上下文消息列表
        logger: 日志记录器实例
    """

    def __init__(
        self, 
        model: Optional[str] = None, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None
    ) -> None:
        """
        Initialize the LLM instance.
        
        Args:
            model: The model name to use (e.g., 'gpt-3.5-turbo', 'gpt-4')
            api_key: OpenAI API key. If None, will use environment variable OPENAI_API_KEY
            base_url: Custom base URL for API calls. If None, uses OpenAI's default
        """
        self.model = model or "gpt-3.5-turbo"
        self.messages: List[Dict[str, str]] = []
        
        # Initialize logger
        self.logger = get_logger(self.__class__.__name__)
        
        # Initialize OpenAI client
        client_kwargs = {}
        if api_key:
            client_kwargs['api_key'] = api_key
        if base_url:
            client_kwargs['base_url'] = base_url
            
        self.client = OpenAI(**client_kwargs)
        
        # Log initialization
        self.logger.info(f"LLM initialized with model: {self.model}")
        if base_url:
            self.logger.info(f"Using custom base URL: {base_url}")

    def chat(
        self, 
        user_input: str, 
        system_prompt: Optional[str] = None, 
        keep_context: bool = True, 
        temperature: float = 0.7
    ) -> str:
        """
        发送用户输入并返回模型回复
        
        Args:
            user_input: 用户本轮输入
            system_prompt: 可选的系统提示，仅首次有效
            keep_context: 是否将本轮对话追加到上下文
            temperature: 生成温度参数，控制回复的随机性
            
        Returns:
            模型回复内容
            
        Raises:
            Exception: 当 API 调用失败时抛出异常
        """
        self.logger.info(f"Starting chat with user input length: {len(user_input)}")
        
        # 首次系统提示
        if system_prompt and not self.messages:
            self.messages.append({"role": "system", "content": system_prompt})
            self.logger.info("Added system prompt to conversation context")

        self.messages.append({"role": "user", "content": user_input})
        self.logger.debug(f"Added user message to context. Total messages: {len(self.messages)}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=temperature,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            assistant_reply = response.choices[0].message.content.strip()
            self.logger.info(f"Received response from model. Reply length: {len(assistant_reply)}")

            if keep_context:
                self.messages.append({"role": "assistant", "content": assistant_reply})
                self.logger.debug("Added assistant reply to context")
            else:
                # 不保留上下文则回滚 user 消息
                self.messages.pop()
                self.logger.debug("Removed user message from context (keep_context=False)")

            return assistant_reply
            
        except Exception as e:
            self.logger.error(f"Error during chat completion: {str(e)}")
            # 如果出错，移除刚添加的用户消息
            if self.messages and self.messages[-1]["role"] == "user":
                self.messages.pop()
                self.logger.debug("Removed user message due to error")
            raise

    def clear_context(self) -> None:
        """清空当前对话上下文"""
        previous_count = len(self.messages)
        self.messages.clear()
        self.logger.info(f"Cleared conversation context. Removed {previous_count} messages")

    def get_context(self) -> List[Dict[str, str]]:
        """
        获取当前对话上下文
        
        Returns:
            当前对话上下文的副本
        """
        self.logger.debug(f"Retrieved conversation context with {len(self.messages)} messages")
        return self.messages.copy()

    def set_context(self, history: List[Dict[str, str]]) -> None:
        """
        手动设置对话上下文
        
        Args:
            history: 要设置的对话历史记录
        """
        previous_count = len(self.messages)
        self.messages = history.copy()
        self.logger.info(f"Set conversation context. Previous: {previous_count}, New: {len(self.messages)} messages")

