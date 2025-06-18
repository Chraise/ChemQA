#!/usr/bin/env python3
"""
重新运行失败问题的脚本

专门重新运行问题7和10，并更新汇总文件。
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.qa_system.expert_system import ChemicalQAExpert
from src.qa_system.citation_analyzer import CitationAnalyzer


class FailedQuestionRerunner:
    """失败问题重新运行器"""
    
    def __init__(self):
        """初始化重新运行器"""
        self.expert_system = ChemicalQAExpert()
        self.citation_analyzer = CitationAnalyzer()
        
        # 定义输出目录
        self.output_dir = Path("qa_testing/test_output")
        
        # 定义需要重新运行的问题
        self.failed_questions = [7, 10]
        
        # 定义问题列表（与原始测试相同）
        self.questions = [
            "What are the key mechanisms of CO2 electroreduction on copper-based catalysts?",
            "How does the coordination environment affect the performance of nickel-based electrocatalysts for alcohol oxidation?",
            "What are the recent advances in electrochemical C-H functionalization of aromatic compounds?",
            "How can we improve the selectivity of electrochemical reduction of carbonyl compounds?",
            "What role do electrolyte additives play in organic electrocatalysis?",
            "How does the surface structure of platinum catalysts influence organic molecule oxidation?",
            "What are the challenges and solutions for electrochemical synthesis of heterocyclic compounds?",
            "How can we achieve high current density in organic electrosynthesis?",
            "What are the mechanistic insights into electrochemical oxidation of biomass-derived compounds?",
            "How does the pH of electrolyte affect the reaction pathways in organic electrocatalysis?"
        ]
    
    def load_existing_summary(self) -> dict:
        """加载现有的汇总文件"""
        summary_file = self.output_dir / "test_summary.json"
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def run_single_question(self, question_id: int) -> dict:
        """运行单个问题"""
        question = self.questions[question_id - 1]  # 转换为0索引
        
        print(f"\n{'='*80}")
        print(f"重新运行问题 {question_id}/10: {question}")
        print(f"{'='*80}")
        
        try:
            # 记录开始时间
            start_time = time.time()
            
            print("正在生成答案...")
            
            # 检索上下文
            context = self.expert_system.retriever.retrieve_relevant_context(question, return_dict_list=True)
            # 使用专家系统生成答案
            answer = self.expert_system.answer_query(question, analyze_citations=False)
            
            # 计算处理时间
            processing_time = time.time() - start_time
            
            # 分析引用
            print("正在分析引用...")
            citation_analysis = self.citation_analyzer.analyze_citations(answer, context)
            
            # 保存答案文件
            answer_file = self.output_dir / f"answer_{question_id:02d}.md"
            with open(answer_file, 'w', encoding='utf-8') as f:
                f.write(f"# 有机电催化问答 - 问题 {question_id}\n\n")
                f.write(f"**问题：** {question}\n\n")
                f.write(f"**回答时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**处理时间：** {processing_time:.2f} 秒\n")
                f.write(f"**方法：** 本地文献库检索 + 专家系统\n\n")
                f.write(f"## 回答内容\n\n{answer}\n\n")
                f.write("---\n")
                f.write("*此回答基于本地文献库检索生成，包含相关文献引用。*")
            
            # 保存引用分析
            citation_file = self.output_dir / f"citation_analysis_{question_id:02d}.txt"
            with open(citation_file, 'w', encoding='utf-8') as f:
                f.write(f"引用分析报告 - 问题 {question_id}\n")
                f.write("="*50 + "\n\n")
                f.write(f"问题: {question}\n\n")
                f.write(f"引用数量: {citation_analysis['cited_chunks_analysis']['cited_count']}\n")
                f.write(f"上下文片段数量: {citation_analysis['total_context_chunks']}\n\n")
                
                if citation_analysis['cited_chunks_analysis']['cited_chunks']:
                    f.write("详细引用信息:\n")
                    for i, chunk in enumerate(citation_analysis['cited_chunks_analysis']['cited_chunks'], 1):
                        f.write(f"\n{i}. 来源: {chunk['source']}  片段号: {chunk['chunk_index']}\n")
                        f.write(f"   内容预览: {chunk['text_preview']}\n")
                else:
                    f.write("未发现引用标记。\n")
            
            # 返回结果
            result = {
                "question_id": question_id,
                "question": question,
                "processing_time": round(processing_time, 2),
                "timestamp": datetime.now().isoformat(),
                "answer_length": len(answer),
                "answer": answer,
                "citation_count": citation_analysis['cited_chunks_analysis']['cited_count'],
                "context_fragments": citation_analysis['total_context_chunks'],
                "method": "retrieval_augmented"
            }
            
            print(f"✅ 问题 {question_id} 重新运行完成")
            print(f"   处理时间: {processing_time:.2f} 秒")
            print(f"   答案长度: {len(answer)} 字符")
            print(f"   引用数量: {citation_analysis['cited_chunks_analysis']['cited_count']}")
            
            return result
            
        except Exception as e:
            print(f"❌ 问题 {question_id} 重新运行失败: {str(e)}")
            return {
                "question_id": question_id,
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "method": "retrieval_augmented"
            }
    
    def update_summary_files(self, new_results: list):
        """更新汇总文件"""
        print("📝 正在更新汇总文件...")
        
        # 读取现有的详细结果
        detailed_results_file = self.output_dir / "detailed_results.json"
        if detailed_results_file.exists():
            with open(detailed_results_file, 'r', encoding='utf-8') as f:
                detailed_results = json.load(f)
        else:
            detailed_results = []
        
        # 更新失败问题的结果
        for new_result in new_results:
            question_id = new_result['question_id']
            # 找到对应的结果并更新
            for i, result in enumerate(detailed_results):
                if result['question_id'] == question_id:
                    detailed_results[i] = new_result
                    break
            else:
                # 如果没找到，添加新结果
                detailed_results.append(new_result)
        
        # 保存更新后的详细结果
        with open(detailed_results_file, 'w', encoding='utf-8') as f:
            json.dump(detailed_results, f, ensure_ascii=False, indent=2)
        
        # 重新计算统计信息
        successful_tests = [r for r in detailed_results if 'error' not in r]
        failed_tests = [r for r in detailed_results if 'error' in r]
        
        # 计算平均指标
        avg_processing_time = sum(r.get('processing_time', 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_answer_length = sum(r.get('answer_length', 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_citation_count = sum(r.get('citation_count', 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_context_fragments = sum(r.get('context_fragments', 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
        
        # 更新JSON汇总文件
        summary_json_file = self.output_dir / "test_summary.json"
        summary_data = {
            "total_questions": len(detailed_results),
            "successful_questions": len(successful_tests),
            "failed_questions": len(failed_tests),
            "average_processing_time": round(avg_processing_time, 2),
            "average_answer_length": round(avg_answer_length, 1),
            "average_citation_count": round(avg_citation_count, 2),
            "average_context_fragments": round(avg_context_fragments, 2),
            "detailed_results": detailed_results
        }
        
        with open(summary_json_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
        # 写入文本报告
        summary_report_file = self.output_dir / "test_summary_report.txt"
        with open(summary_report_file, 'w', encoding='utf-8') as f:
            f.write(f"有机电催化问答测试汇总报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"总问题数: {len(detailed_results)}\n")
            f.write(f"成功问题数: {len(successful_tests)}\n")
            f.write(f"失败问题数: {len(failed_tests)}\n\n")
            f.write(f"平均处理时间: {avg_processing_time:.2f} 秒\n")
            f.write(f"平均答案长度: {avg_answer_length:.1f} 字符\n")
            f.write(f"平均引用片段数: {avg_citation_count:.2f} 个\n")
            f.write(f"平均上下文片段数: {avg_context_fragments:.2f} 个\n\n")
            f.write("详细结果：\n")
            for result in detailed_results:
                f.write(f"\n问题 {result['question_id']}: {result['question']}\n")
                f.write(f"状态: {'成功' if 'error' not in result else '失败'}\n")
                f.write(f"处理时间: {result.get('processing_time', 0):.2f} 秒\n")
                f.write(f"答案长度: {result.get('answer_length', 0):.1f} 字符\n")
                f.write(f"引用数量: {result.get('citation_count', 0)} 个\n")
                f.write(f"上下文片段数: {result.get('context_fragments', 0)} 个\n")
                if 'error' in result:
                    f.write(f"错误信息: {result['error']}\n")
                f.write("-" * 50)
        
        print("✅ 汇总文件更新完成")
    
    def run_failed_questions(self):
        """运行失败的问题"""
        print("🔄 重新运行失败问题")
        print("="*60)
        print(f"📝 需要重新运行的问题: {self.failed_questions}")
        print(f"📁 输出目录: {self.output_dir}")
        
        new_results = []
        
        for question_id in self.failed_questions:
            result = self.run_single_question(question_id)
            new_results.append(result)
            
            # 添加延迟避免API限制
            if question_id != self.failed_questions[-1]:
                print("⏳ 等待5秒后继续下一个问题...")
                time.sleep(5)
        
        # 更新汇总文件
        self.update_summary_files(new_results)
        
        # 打印汇总信息
        successful_reruns = [r for r in new_results if 'error' not in r]
        failed_reruns = [r for r in new_results if 'error' in r]
        
        print(f"\n📈 重新运行汇总:")
        print(f"   成功: {len(successful_reruns)}/{len(self.failed_questions)}")
        print(f"   失败: {len(failed_reruns)}/{len(self.failed_questions)}")
        
        if failed_reruns:
            print(f"\n❌ 仍然失败的问题:")
            for result in failed_reruns:
                print(f"   问题 {result['question_id']}: {result['error']}")
        
        print(f"\n🎉 重新运行完成！")


def main():
    """主函数"""
    print("🔄 失败问题重新运行脚本")
    print("="*60)
    print("🔧 专门处理API超时的问题7和10")
    
    # 创建重新运行器并执行
    rerunner = FailedQuestionRerunner()
    rerunner.run_failed_questions()


if __name__ == "__main__":
    main() 