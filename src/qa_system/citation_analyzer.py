import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from src.utils.logger import logger


class CitationAnalyzer:
    """
    分析答案引用的上下文片段数量的工具类
    """
    
    def __init__(self):
        """初始化引用分析器"""
        pass
    
    def analyze_citations(self, answer: str, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析答案中的引用情况
        
        Args:
            answer: 原始答案文本
            context: 上下文片段列表
            
        Returns:
            包含引用分析结果的字典
        """
        logger.info("开始分析答案引用情况")
        
        # 1. 统计上下文片段总数
        total_context_chunks = len(context)
        
        # 2. 提取答案中的所有引用标记
        citations_in_answer = self._extract_citations_from_answer(answer)
        
        # 3. 分析引用的上下文片段
        cited_chunks_analysis = self._analyze_cited_chunks(answer, context)
        
        # 4. 计算引用覆盖率
        citation_coverage = self._calculate_coverage(cited_chunks_analysis, total_context_chunks)
        
        # 5. 生成详细报告
        analysis_report = {
            "total_context_chunks": total_context_chunks,
            "citations_in_answer": citations_in_answer,
            "cited_chunks_analysis": cited_chunks_analysis,
            "citation_coverage": citation_coverage,
            "summary": self._generate_summary(cited_chunks_analysis, citation_coverage)
        }
        
        logger.info(f"引用分析完成: 总片段{total_context_chunks}个, 引用片段{citation_coverage['cited_count']}个")
        return analysis_report
    
    def _extract_citations_from_answer(self, answer: str) -> List[str]:
        """
        从答案中提取所有引用标记
        
        Args:
            answer: 答案文本
            
        Returns:
            引用标记列表
        """
        # 匹配各种引用格式
        citation_patterns = [
            r'\[Ref\s+([^\]]+)\]',  # [Ref xxx]
            r'\[(\d+)\]',          # [1], [2], [3]...
            r'\[([^\]]+)\]'        # 其他格式的引用
        ]
        
        citations = []
        for pattern in citation_patterns:
            matches = re.findall(pattern, answer)
            citations.extend(matches)
        
        # 去重并返回
        return list(set(citations))
    
    def _analyze_cited_chunks(self, answer: str, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析被引用的上下文片段
        
        Args:
            answer: 答案文本
            context: 上下文片段列表
            
        Returns:
            引用分析结果
        """
        # 建立上下文片段的映射
        chunk_mapping = {}
        for i, doc in enumerate(context):
            # 获取片段标识符
            chunk_id = None
            if isinstance(doc, dict):
                if 'chunk_index' in doc:
                    chunk_id = f"chunk_{doc['chunk_index']}"
                elif 'source' in doc:
                    chunk_id = f"source_{doc['source']}"
                else:
                    chunk_id = f"chunk_{i}"
            
            chunk_mapping[chunk_id] = {
                "index": i,
                "source": doc.get('source', 'unknown'),
                "chunk_index": doc.get('chunk_index', i),
                "text_preview": doc.get('text', '')[:100] + "..." if doc.get('text') else "",
                "cited": False,
                "citation_count": 0
            }
        
        # 检查每个片段是否被引用
        cited_chunks = []
        for chunk_id, chunk_info in chunk_mapping.items():
            # 检查答案中是否包含对该片段的引用
            citation_patterns = [
                f"[Ref {chunk_info['chunk_index']}]",
                f"[Ref {chunk_info['source']}]",
                f"[Ref {chunk_id}]"
            ]
            
            for pattern in citation_patterns:
                if pattern in answer:
                    chunk_info['cited'] = True
                    chunk_info['citation_count'] = answer.count(pattern)
                    cited_chunks.append(chunk_info)
                    break
        
        return {
            "total_chunks": len(context),
            "cited_chunks": cited_chunks,
            "cited_count": len(cited_chunks),
            "chunk_mapping": chunk_mapping
        }
    
    def _calculate_coverage(self, cited_chunks_analysis: Dict[str, Any], total_chunks: int) -> Dict[str, Any]:
        """
        计算引用覆盖率
        
        Args:
            cited_chunks_analysis: 引用分析结果
            total_chunks: 总片段数
            
        Returns:
            覆盖率统计
        """
        cited_count = cited_chunks_analysis['cited_count']
        coverage_percentage = (cited_count / total_chunks * 100) if total_chunks > 0 else 0
        
        return {
            "cited_count": cited_count,
            "total_count": total_chunks,
            "coverage_percentage": round(coverage_percentage, 2),
            "unused_count": total_chunks - cited_count
        }
    
    def _generate_summary(self, cited_chunks_analysis: Dict[str, Any], coverage: Dict[str, Any]) -> str:
        """
        生成分析摘要
        
        Args:
            cited_chunks_analysis: 引用分析结果
            coverage: 覆盖率统计
            
        Returns:
            摘要文本
        """
        summary = f"引用分析摘要:\n"
        summary += f"- 总上下文片段数: {coverage['total_count']}\n"
        summary += f"- 被引用的片段数: {coverage['cited_count']}\n"
        summary += f"- 未使用的片段数: {coverage['unused_count']}\n"
        summary += f"- 引用覆盖率: {coverage['coverage_percentage']}%\n"
        
        if cited_chunks_analysis['cited_chunks']:
            summary += f"- 被引用的片段来源: "
            sources = list(set(chunk['source'] for chunk in cited_chunks_analysis['cited_chunks']))
            summary += ", ".join(sources[:5])  # 只显示前5个来源
            if len(sources) > 5:
                summary += f" 等{len(sources)}个来源"
        
        return summary
    
    def print_detailed_report(self, analysis_report: Dict[str, Any]) -> None:
        """
        打印详细的分析报告
        
        Args:
            analysis_report: 分析报告
        """
        print("\n" + "="*60)
        print("答案引用上下文片段分析报告")
        print("="*60)
        
        # 基本信息
        print(f"\n📊 基本统计:")
        print(f"   总上下文片段数: {analysis_report['total_context_chunks']}")
        print(f"   被引用的片段数: {analysis_report['citation_coverage']['cited_count']}")
        print(f"   引用覆盖率: {analysis_report['citation_coverage']['coverage_percentage']}%")
        
        # 引用详情
        if analysis_report['cited_chunks_analysis']['cited_chunks']:
            print(f"\n📚 被引用的片段详情:")
            for i, chunk in enumerate(analysis_report['cited_chunks_analysis']['cited_chunks'], 1):
                print(f"   {i}. 来源: {chunk['source']}")
                print(f"      片段索引: {chunk['chunk_index']}")
                print(f"      引用次数: {chunk['citation_count']}")
                print(f"      内容预览: {chunk['text_preview']}")
                print()
        
        # 未使用的片段
        unused_count = analysis_report['citation_coverage']['unused_count']
        if unused_count > 0:
            print(f"\n⚠️  未使用的片段:")
            print(f"   有 {unused_count} 个上下文片段未被引用")
            
            # 显示一些未使用的片段
            unused_chunks = []
            for chunk_id, chunk_info in analysis_report['cited_chunks_analysis']['chunk_mapping'].items():
                if not chunk_info['cited']:
                    unused_chunks.append(chunk_info)
            
            for i, chunk in enumerate(unused_chunks[:3], 1):  # 只显示前3个
                print(f"   {i}. 来源: {chunk['source']}")
                print(f"      内容预览: {chunk['text_preview']}")
                print()
            
            if len(unused_chunks) > 3:
                print(f"   ... 还有 {len(unused_chunks) - 3} 个未使用的片段")
        
        # 摘要
        print(f"\n📋 分析摘要:")
        print(analysis_report['summary'])
        
        print("\n" + "="*60)
    
    def save_analysis_to_file(self, analysis_report: Dict[str, Any], filename: str = "citation_analysis.txt") -> None:
        """
        将分析结果保存到文件
        
        Args:
            analysis_report: 分析报告
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("答案引用上下文片段分析报告\n")
                f.write("="*50 + "\n\n")
                
                # 写入摘要
                f.write(analysis_report['summary'] + "\n\n")
                
                # 写入详细统计
                f.write("详细统计:\n")
                f.write(f"总上下文片段数: {analysis_report['total_context_chunks']}\n")
                f.write(f"被引用的片段数: {analysis_report['citation_coverage']['cited_count']}\n")
                f.write(f"引用覆盖率: {analysis_report['citation_coverage']['coverage_percentage']}%\n\n")
                
                # 写入被引用的片段详情
                if analysis_report['cited_chunks_analysis']['cited_chunks']:
                    f.write("被引用的片段详情:\n")
                    for i, chunk in enumerate(analysis_report['cited_chunks_analysis']['cited_chunks'], 1):
                        f.write(f"{i}. 来源: {chunk['source']}\n")
                        f.write(f"   片段索引: {chunk['chunk_index']}\n")
                        f.write(f"   引用次数: {chunk['citation_count']}\n")
                        f.write(f"   内容预览: {chunk['text_preview']}\n\n")
            
            logger.info(f"引用分析报告已保存到: {filename}")
        except Exception as e:
            logger.error(f"保存分析报告失败: {str(e)}")


def analyze_answer_citations(answer: str, context: List[Dict[str, Any]], 
                           print_report: bool = True, save_to_file: bool = False) -> Dict[str, Any]:
    """
    便捷函数：分析答案引用的上下文片段数量
    
    Args:
        answer: 答案文本
        context: 上下文片段列表
        print_report: 是否打印报告
        save_to_file: 是否保存到文件
        
    Returns:
        分析报告字典
    """
    analyzer = CitationAnalyzer()
    analysis_report = analyzer.analyze_citations(answer, context)
    
    if print_report:
        analyzer.print_detailed_report(analysis_report)
    
    if save_to_file:
        analyzer.save_analysis_to_file(analysis_report)
    
    return analysis_report 