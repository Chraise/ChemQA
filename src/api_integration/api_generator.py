from config.prompts import ORGANIC_ELECTROCATALYSIS_PROMPT
from config.settings import settings
from src.api_integration.api_handler import DeepSeekAPIHandler


class DeepSeekAnswerGenerator:
    def __init__(self):
        self.api_handler = DeepSeekAPIHandler()
        self.prompt_template = ORGANIC_ELECTROCATALYSIS_PROMPT

    def generate_answer(self, question: str, context: str) -> str:
        """生成基于上下文的专业回答"""
        # 构建完整提示
        full_prompt = self._build_prompt(question, context)

        # 调用DeepSeek API
        response = self.api_handler.generate_response(full_prompt)

        return response

    def _build_prompt(self, question: str, context: str) -> str:
        """整合提示模板"""
        return self.prompt_template.format(
            domain=settings.DOMAIN,
            context=context,
            question=question
        )
