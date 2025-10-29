from openai import OpenAI
from typing import Optional, List, Dict, Any

from src.core.base.logger import get_logger


class LLM:
    """
    支持上下文对话的 LLM 封装类
    默认使用 OpenAI GPT 系列模型，可扩展其他后端

    属性:
        model: 模型名称
        messages: 对话上下文消息列表
        logger: 日志记录器实例
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        初始化 LLM 实例

        参数:
            model: 要使用的模型名称（例如：'gpt-3.5-turbo', 'gpt-4'）
            api_key: OpenAI API 密钥。如果为 None，将使用环境变量 OPENAI_API_KEY
            base_url: API 调用的自定义基础 URL。如果为 None，使用 OpenAI 的默认 URL
        """
        self.model = model or "gpt-3.5-turbo"
        self.messages: List[Dict[str, str]] = []

        # 初始化日志记录器
        self.logger = get_logger(self.__class__.__name__)

        # 初始化 OpenAI 客户端
        client_kwargs = {}
        if api_key:
            client_kwargs["api_key"] = api_key
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = OpenAI(**client_kwargs)

        # 记录初始化日志
        self.logger.info(f"LLM 已初始化，使用模型: {self.model}")
        if base_url:
            self.logger.info(f"使用自定义基础 URL: {base_url}")

    def chat(
        self,
        user_input: str,
        system_prompt: Optional[str] = None,
        keep_context: bool = True,
        temperature: float = 0.7,
    ) -> str:
        """
        发送用户输入并返回模型回复

        参数:
            user_input: 用户本轮输入
            system_prompt: 可选的系统提示，仅首次有效
            keep_context: 是否将本轮对话追加到上下文
            temperature: 生成温度参数，控制回复的随机性

        返回:
            模型回复内容

        异常:
            Exception: 当 API 调用失败时抛出异常
        """
        self.logger.info(f"开始对话，用户输入长度: {len(user_input)}")

        # 首次系统提示
        if system_prompt and not self.messages:
            self.messages.append({"role": "system", "content": system_prompt})
            self.logger.info("已添加系统提示到对话上下文")

        self.messages.append({"role": "user", "content": user_input})
        self.logger.debug(f"已添加用户消息到上下文。总消息数: {len(self.messages)}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=temperature,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            assistant_reply = response.choices[0].message.content.strip()
            self.logger.info(f"收到模型回复。回复长度: {len(assistant_reply)}")

            if keep_context:
                self.messages.append({"role": "assistant", "content": assistant_reply})
                self.logger.debug("已添加助手回复到上下文")
            else:
                # 不保留上下文则回滚 user 消息
                self.messages.pop()
                self.logger.debug("已移除用户消息（keep_context=False）")

            return assistant_reply

        except Exception as e:
            self.logger.error(f"对话完成过程中出错: {str(e)}")
            # 如果出错，移除刚添加的用户消息
            if self.messages and self.messages[-1]["role"] == "user":
                self.messages.pop()
                self.logger.debug("由于错误已移除用户消息")
            raise

    def delete_last_qa(self) -> bool:
        """
        删除上一条问答对话（用户问题和助手回答）

        返回:
            bool: 如果成功删除返回 True，如果没有可删除的问答对返回 False
        """
        self.logger.info("尝试删除上一条问答对话")

        # 检查是否有足够的消息可以删除
        if len(self.messages) < 2:
            self.logger.warning("没有足够的消息可以删除问答对")
            return False

        # 查找最后一对用户-助手消息
        deleted_count = 0

        # 从后往前查找，删除最后的助手回复
        if self.messages and self.messages[-1]["role"] == "assistant":
            removed_message = self.messages.pop()
            deleted_count += 1
            self.logger.debug(f"已删除助手回复: {removed_message['content'][:50]}...")

        # 删除对应的用户问题
        if self.messages and self.messages[-1]["role"] == "user":
            removed_message = self.messages.pop()
            deleted_count += 1
            self.logger.debug(f"已删除用户问题: {removed_message['content'][:50]}...")

        if deleted_count > 0:
            self.logger.info(f"成功删除上一条问答对话，删除了 {deleted_count} 条消息")
            return True
        else:
            self.logger.warning("未找到可删除的问答对")
            return False

    def clear_context(self) -> None:
        """清空当前对话上下文"""
        previous_count = len(self.messages)
        self.messages.clear()
        self.logger.info(f"已清空对话上下文。移除了 {previous_count} 条消息")

    def get_context(self) -> List[Dict[str, str]]:
        """
        获取当前对话上下文

        返回:
            当前对话上下文的副本
        """
        self.logger.debug(f"获取对话上下文，包含 {len(self.messages)} 条消息")
        return self.messages.copy()

    def set_context(self, history: List[Dict[str, str]]) -> None:
        """
        手动设置对话上下文

        参数:
            history: 要设置的对话历史记录
        """
        previous_count = len(self.messages)
        self.messages = history.copy()
        self.logger.info(
            f"已设置对话上下文。之前: {previous_count} 条，现在: {len(self.messages)} 条消息"
        )

