#!/usr/bin/env python3
"""
有机电催化问答测试脚本

生成10个英文的有机电催化领域问题，获取回答并进行引用分析。
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
from src.qa_system.citation_analyzer import analyze_answer_citations


class OrganicElectrocatalysisQATester:
    """有机电催化问答测试器"""
    
    def __init__(self):
        """初始化测试器"""
        self.expert = ChemicalQAExpert()
        self.results = []
        
        # 创建输出目录
        self.output_dir = Path("test_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # 定义10个有机电催化领域的问题
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
    
    def run_single_test(self, question: str, question_id: int) -> dict:
        """运行单个问答测试"""
        print(f"\n{'='*80}")
        print(f"测试 {question_id}/10: {question}")
        print(f"{'='*80}")
        
        try:
            # 记录开始时间
            start_time = time.time()
            
            # 获取答案（不进行引用分析，因为我们需要原始答案和上下文）
            print("正在生成答案...")
            
            # 检索相关上下文
            context = self.expert.retriever.retrieve_relevant_context(question, return_dict_list=True)
            
            # 生成原始答案
            raw_answer = self.expert.generator.generate_answer(question, context)
            
            # 分析引用情况
            print("正在分析引用情况...")
            analysis_report = analyze_answer_citations(
                answer=raw_answer,
                context=context,
                print_report=False,  # 不打印详细报告，只返回结果
                save_to_file=False
            )
            
            # 格式化答案
            formatted_response = self.expert.formatter.format(question, raw_answer, context)
            
            # 计算处理时间
            processing_time = time.time() - start_time
            
            # 保存结果
            result = {
                "question_id": question_id,
                "question": question,
                "processing_time": round(processing_time, 2),
                "timestamp": datetime.now().isoformat(),
                "citation_analysis": analysis_report,
                "context_count": len(context),
                "answer_length": len(raw_answer),
                "formatted_answer": formatted_response
            }
            
            # 保存单个测试的答案文件
            answer_file = self.output_dir / f"answer_{question_id:02d}.md"
            with open(answer_file, 'w', encoding='utf-8') as f:
                f.write(formatted_response)
            
            # 保存单个测试的引用分析
            analysis_file = self.output_dir / f"citation_analysis_{question_id:02d}.txt"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write(f"Question {question_id}: {question}\n")
                f.write("="*60 + "\n\n")
                f.write(f"Processing Time: {processing_time:.2f} seconds\n")
                f.write(f"Context Chunks: {len(context)}\n")
                f.write(f"Answer Length: {len(raw_answer)} characters\n\n")
                f.write("Citation Analysis Summary:\n")
                f.write(f"- Total Context Chunks: {analysis_report['total_context_chunks']}\n")
                f.write(f"- Cited Chunks: {analysis_report['citation_coverage']['cited_count']}\n")
                f.write(f"- Citation Coverage: {analysis_report['citation_coverage']['coverage_percentage']}%\n")
                f.write(f"- Unused Chunks: {analysis_report['citation_coverage']['unused_count']}\n\n")
                
                if analysis_report['cited_chunks_analysis']['cited_chunks']:
                    f.write("Cited Chunks Details:\n")
                    for i, chunk in enumerate(analysis_report['cited_chunks_analysis']['cited_chunks'], 1):
                        f.write(f"{i}. Source: {chunk['source']}\n")
                        f.write(f"   Chunk Index: {chunk['chunk_index']}\n")
                        f.write(f"   Citation Count: {chunk['citation_count']}\n")
                        f.write(f"   Content Preview: {chunk['text_preview']}\n\n")
            
            print(f"✅ 测试 {question_id} 完成")
            print(f"   处理时间: {processing_time:.2f} 秒")
            print(f"   上下文片段: {len(context)} 个")
            print(f"   引用覆盖率: {analysis_report['citation_coverage']['coverage_percentage']}%")
            
            return result
            
        except Exception as e:
            print(f"❌ 测试 {question_id} 失败: {str(e)}")
            return {
                "question_id": question_id,
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始有机电催化问答测试")
        print(f"📝 总共 {len(self.questions)} 个问题")
        print(f"📁 输出目录: {self.output_dir}")
        
        start_time = time.time()
        
        for i, question in enumerate(self.questions, 1):
            result = self.run_single_test(question, i)
            self.results.append(result)
            
            # 添加延迟避免API限制
            if i < len(self.questions):
                print("⏳ 等待3秒后继续下一个测试...")
                time.sleep(3)
        
        total_time = time.time() - start_time
        
        # 保存汇总结果
        self.save_summary_results(total_time)
        
        print(f"\n🎉 所有测试完成！总耗时: {total_time:.2f} 秒")
        print(f"📊 结果已保存到: {self.output_dir}")
    
    def save_summary_results(self, total_time: float):
        """保存汇总结果"""
        # 计算统计信息
        successful_tests = [r for r in self.results if 'error' not in r]
        failed_tests = [r for r in self.results if 'error' in r]
        
        # 计算平均指标
        avg_processing_time = sum(r['processing_time'] for r in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_context_count = sum(r['context_count'] for r in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_citation_coverage = sum(r['citation_analysis']['citation_coverage']['coverage_percentage'] for r in successful_tests) / len(successful_tests) if successful_tests else 0
        
        # 保存JSON格式的汇总结果
        summary_data = {
            "test_info": {
                "total_questions": len(self.questions),
                "successful_tests": len(successful_tests),
                "failed_tests": len(failed_tests),
                "total_time": round(total_time, 2),
                "timestamp": datetime.now().isoformat()
            },
            "statistics": {
                "avg_processing_time": round(avg_processing_time, 2),
                "avg_context_count": round(avg_context_count, 1),
                "avg_citation_coverage": round(avg_citation_coverage, 2)
            },
            "detailed_results": self.results
        }
        
        # 保存JSON文件
        json_file = self.output_dir / "test_summary.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
        # 保存文本格式的汇总报告
        report_file = self.output_dir / "test_summary_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("有机电催化问答测试汇总报告\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总问题数: {len(self.questions)}\n")
            f.write(f"成功测试: {len(successful_tests)}\n")
            f.write(f"失败测试: {len(failed_tests)}\n")
            f.write(f"总耗时: {total_time:.2f} 秒\n\n")
            
            f.write("统计信息:\n")
            f.write(f"- 平均处理时间: {avg_processing_time:.2f} 秒\n")
            f.write(f"- 平均上下文片段数: {avg_context_count:.1f}\n")
            f.write(f"- 平均引用覆盖率: {avg_citation_coverage:.2f}%\n\n")
            
            f.write("详细结果:\n")
            for result in self.results:
                f.write(f"\n问题 {result['question_id']}: {result['question']}\n")
                if 'error' in result:
                    f.write(f"状态: 失败 - {result['error']}\n")
                else:
                    f.write(f"状态: 成功\n")
                    f.write(f"处理时间: {result['processing_time']} 秒\n")
                    f.write(f"上下文片段: {result['context_count']} 个\n")
                    f.write(f"引用覆盖率: {result['citation_analysis']['citation_coverage']['coverage_percentage']}%\n")
                    f.write(f"答案长度: {result['answer_length']} 字符\n")
        
        # 打印汇总信息
        print(f"\n📈 测试汇总:")
        print(f"   成功: {len(successful_tests)}/{len(self.questions)}")
        print(f"   失败: {len(failed_tests)}/{len(self.questions)}")
        print(f"   平均处理时间: {avg_processing_time:.2f} 秒")
        print(f"   平均引用覆盖率: {avg_citation_coverage:.2f}%")
        
        if failed_tests:
            print(f"\n❌ 失败的测试:")
            for test in failed_tests:
                print(f"   问题 {test['question_id']}: {test['error']}")


def main():
    """主函数"""
    print("🧪 有机电催化问答测试脚本")
    print("="*60)
    
    # 创建测试器并运行测试
    tester = OrganicElectrocatalysisQATester()
    tester.run_all_tests()


if __name__ == "__main__":
    main() 