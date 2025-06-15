import os
import re
from datetime import datetime
from typing import List, Dict, Any

from config.settings import settings
from src.utils.logger import logger


class ResponseFormatter:
    def __init__(self):
        self.system_domain = settings.DOMAIN

    def format(self, question: str, answer: str, context: List[Dict[str, Any]]) -> str:
        """格式化响应"""

        # 使用format_answer方法处理引用和参考文献
        formatted = self.format_answer(answer, context)

        # 构建响应头
        response = f"# 有机电催化专家系统\n\n"
        response += f"**问题：** {question}\n\n"
        response += f"**回答日期：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        response += f"**模型：** {settings.DEEPSEEK_API_CONFIG['model']}\n\n"

        # 添加主要回答
        response += f"## 问题分析\n{formatted['formatted_answer']}\n\n"

        # 添加参考文献
        response += f"## 参考文献\n{chr(10).join(formatted['citations']) if formatted['citations'] else '无'}\n\n"

        # 添加上下文摘要
        response += f"*注：本回答综合了{formatted['num_references']}篇相关研究文献的见解*\n\n"

        # 添加响应结束标记
        response += "---\n"
        response += "*回答由有机电催化专家系统生成，使用DeepSeek AI和专业的有机电催化知识库。*"

        logger.info("已格式化用户响应")
        return response

    def format_answer(self, answer: str, context: List[Dict[str, Any]]) -> dict:
        logger.info(f"format_answer收到的context: {context}")
        # 1. 为每个PDF分配唯一编号，并建立source到编号的映射
        unique_pdfs = []
        source_to_num = {}
        for doc in context:
            pdf_name = None
            if isinstance(doc, dict) and 'source' in doc:
                pdf_name = doc['source']
            elif isinstance(doc, dict) and 'metadata' in doc and 'source' in doc['metadata']:
                pdf_name = doc['metadata']['source']
            if pdf_name and pdf_name.endswith('.pdf') and pdf_name not in unique_pdfs:
                unique_pdfs.append(pdf_name)
        for idx, pdf in enumerate(unique_pdfs, 1):
            source_to_num[pdf] = idx
        valid_ref_nums = set(str(i) for i in range(1, len(unique_pdfs) + 1))

        # 2. 建立chunk_index到PDF编号的映射（用于替换[Ref xx]）
        chunk_ref_map = {}
        for doc in context:
            pdf_name = None
            if isinstance(doc, dict) and 'source' in doc:
                pdf_name = doc['source']
            elif isinstance(doc, dict) and 'metadata' in doc and 'source' in doc['metadata']:
                pdf_name = doc['metadata']['source']
            if pdf_name and pdf_name.endswith('.pdf'):
                ref_num = source_to_num.get(pdf_name)
                # 支持[Ref chunk_index]和[Ref pdf_name]两种替换
                if 'chunk_index' in doc:
                    chunk_ref_map[f"[Ref {doc['chunk_index']}]"] = f"[{ref_num}]"
                chunk_ref_map[f"[Ref {pdf_name}]"] = f"[{ref_num}]"

        # 3. 替换正文中的所有[Ref ...]为统一编号
        formatted_answer = answer
        for k, v in chunk_ref_map.items():
            formatted_answer = formatted_answer.replace(k, v)

        # 3.1 清理所有context外的引用编号
        formatted_answer = re.sub(r"\[Ref [^\]]+\]", "", formatted_answer)

        def ref_filter(m):
            num = m.group(1)
            return f'[{num}]' if num in valid_ref_nums else ''

        formatted_answer = re.sub(r'\[(\d+)\]', ref_filter, formatted_answer)

        # 3.2 清理正文中大模型生成的"引用文献"或"参考文献"区块（直接删除整个区块）
        bib_pattern = r'(\*\*引用文献\*\*|\*\*参考文献\*\*|\*\*引用标注\*\*|引用文献|参考文献|引用标注)[^#\n]*((\n|.)*?)(?=(\n##|\n#|\Z))'
        formatted_answer = re.sub(bib_pattern, '', formatted_answer, flags=re.MULTILINE)

        # 4. 处理段落和列表的换行
        formatted_answer = re.sub(r'([^\n])\n([^\n])', r'\1  \n\2', formatted_answer)
        formatted_answer = re.sub(r'(- .*?)(\n|$)', r'\1  \n', formatted_answer)

        # 5. 构建参考文献列表
        citations = []
        for pdf in unique_pdfs:
            # 从文件路径中提取纯文件名（不含目录）
            filename = os.path.basename(pdf)

            # 移除文件扩展名（如.pdf）
            # 保留所有其他内容（包括年份、标题等）
            filename_without_ext = os.path.splitext(filename)[0]

            # 直接使用文件名作为引用内容
            citations.append(f"[{source_to_num[pdf]}] {filename_without_ext}  ")

        response = {
            "formatted_answer": formatted_answer,
            "citations": citations,
            "num_references": len(unique_pdfs)
        }
        logger.info(f"已格式化用户响应，包含{len(unique_pdfs)}篇参考文献")
        return response
