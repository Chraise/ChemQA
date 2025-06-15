from src.knowledge_base.retriever import Retriever
from src.api_integration.api_generator import DeepSeekAnswerGenerator  # 修改为DeepSeek生成器
from src.qa_system.response_formatter import ResponseFormatter
from src.utils.logger import logger
import subprocess
import os
import shutil
from pathlib import Path


class ChemicalQAExpert:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = DeepSeekAnswerGenerator()
        self.formatter = ResponseFormatter()
        logger.info(f"System initialized!")

    def answer_query(self, question: str) -> str:
        """回答用户问题"""
        # 检索相关上下文
        context = self.retriever.retrieve_relevant_context(question, return_dict_list=True)
        
        # 生成专业回答
        raw_answer = self.generator.generate_answer(question, context)
        
        # 格式化回答
        formatted_response = self.formatter.format(question, raw_answer, context)
        
        # 保存回答到文件
        self._save_answer(formatted_response)
        
        return formatted_response

    def _save_answer(self, answer: str):
        """保存回答为Markdown文件"""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        md_file = output_dir / "answer.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(answer)
        logger.info(f"回答已保存为 {md_file}")