from src.knowledge_base.retriever import Retriever
from src.api_integration.api_generator import DeepSeekAnswerGenerator  # 修改为DeepSeek生成器
from src.qa_system.response_formatter import ResponseFormatter
from src.qa_system.citation_analyzer import CitationAnalyzer
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
        self.citation_analyzer = CitationAnalyzer()
        logger.info(f"System initialized!")

    def answer_query(self, question: str, analyze_citations: bool = True) -> str:
        """回答用户问题"""
        # 检索相关上下文
        context = self.retriever.retrieve_relevant_context(question, return_dict_list=True)
        
        # 生成专业回答
        raw_answer = self.generator.generate_answer(question, context)
        
        # 分析引用情况（如果启用）
        if analyze_citations and context:
            self._analyze_citations(raw_answer, context)
        
        # 格式化回答
        formatted_response = self.formatter.format(question, raw_answer, context)
        
        # 保存回答到文件
        self._save_answer(formatted_response)
        
        return formatted_response

    def _analyze_citations(self, answer: str, context: list):
        """分析答案的引用情况"""
        try:
            logger.info("开始分析答案引用情况")
            
            # 使用引用分析器
            analysis_report = self.citation_analyzer.analyze_citations(answer, context)
            
            # 打印分析报告
            self.citation_analyzer.print_detailed_report(analysis_report)
            
            # 保存分析报告
            self.citation_analyzer.save_analysis_to_file(analysis_report, "output/citation_analysis.txt")
            
            logger.info("引用分析完成")
            
        except Exception as e:
            logger.error(f"引用分析失败: {str(e)}")

    def _save_answer(self, answer: str):
        """保存回答为Markdown文件"""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        md_file = output_dir / "answer.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(answer)
        logger.info(f"回答已保存为 {md_file}")

    def analyze_existing_answer(self, answer_file: str = "output/answer.md"):
        """分析现有答案文件的引用情况"""
        try:
            # 检查文件是否存在
            if not os.path.exists(answer_file):
                logger.error(f"答案文件不存在: {answer_file}")
                return None
            
            # 读取答案文件
            with open(answer_file, 'r', encoding='utf-8') as f:
                answer_content = f.read()
            
            # 提取问题分析部分
            import re
            analysis_match = re.search(r'## 问题分析\n(.*?)\n\n## 参考文献', answer_content, re.DOTALL)
            
            if not analysis_match:
                logger.error("无法从答案文件中提取问题分析内容")
                return None
            
            analysis = analysis_match.group(1).strip()
            
            # 由于无法从格式化后的答案中恢复原始上下文，
            # 这里提供一个简化的分析，只统计引用标记
            logger.info("分析现有答案文件的引用情况")
            
            # 提取所有引用标记
            citations = re.findall(r'\[(\d+)\]', analysis)
            unique_citations = list(set(citations))
            
            print(f"\n引用分析结果:")
            print(f"总引用次数: {len(citations)}")
            print(f"唯一引用数: {len(unique_citations)}")
            print(f"引用的文献编号: {sorted(unique_citations, key=int)}")
            
            return {
                "total_citations": len(citations),
                "unique_citations": len(unique_citations),
                "citation_numbers": sorted(unique_citations, key=int)
            }
            
        except Exception as e:
            logger.error(f"分析现有答案失败: {str(e)}")
            return None