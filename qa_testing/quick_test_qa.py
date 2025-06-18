#!/usr/bin/env python3
"""
快速有机电催化问答测试脚本

测试前3个英文的有机电催化领域问题，获取回答并进行引用分析。
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


def quick_test():
    """快速测试前3个问题"""
    
    # 定义前3个问题
    questions = [
        "What are the key mechanisms of CO2 electroreduction on copper-based catalysts?",
        "How does the coordination environment affect the performance of nickel-based electrocatalysts for alcohol oxidation?",
        "What are the recent advances in electrochemical C-H functionalization of aromatic compounds?"
    ]
    
    # 创建输出目录
    output_dir = Path("quick_test_output")
    output_dir.mkdir(exist_ok=True)
    
    print("🧪 快速有机电催化问答测试")
    print("="*60)
    print(f"📝 测试 {len(questions)} 个问题")
    print(f"📁 输出目录: {output_dir}")
    
    expert = ChemicalQAExpert()
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"测试 {i}/3: {question}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            
            print("正在生成答案...")
            
            # 检索相关上下文
            context = expert.retriever.retrieve_relevant_context(question, return_dict_list=True)
            
            # 生成原始答案
            raw_answer = expert.generator.generate_answer(question, context)
            
            # 分析引用情况
            print("正在分析引用情况...")
            analysis_report = analyze_answer_citations(
                answer=raw_answer,
                context=context,
                print_report=False,
                save_to_file=False
            )
            
            # 格式化答案
            formatted_response = expert.formatter.format(question, raw_answer, context)
            
            processing_time = time.time() - start_time
            
            # 保存结果
            result = {
                "question_id": i,
                "question": question,
                "processing_time": round(processing_time, 2),
                "timestamp": datetime.now().isoformat(),
                "citation_analysis": analysis_report,
                "context_count": len(context),
                "answer_length": len(raw_answer)
            }
            
            # 保存答案文件
            answer_file = output_dir / f"answer_{i:02d}.md"
            with open(answer_file, 'w', encoding='utf-8') as f:
                f.write(formatted_response)
            
            # 保存引用分析
            analysis_file = output_dir / f"citation_analysis_{i:02d}.txt"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write(f"Question {i}: {question}\n")
                f.write("="*50 + "\n\n")
                f.write(f"Processing Time: {processing_time:.2f} seconds\n")
                f.write(f"Context Chunks: {len(context)}\n")
                f.write(f"Answer Length: {len(raw_answer)} characters\n\n")
                f.write("Citation Analysis:\n")
                f.write(f"- Total Context Chunks: {analysis_report['total_context_chunks']}\n")
                f.write(f"- Cited Chunks: {analysis_report['citation_coverage']['cited_count']}\n")
                f.write(f"- Citation Coverage: {analysis_report['citation_coverage']['coverage_percentage']}%\n")
                f.write(f"- Unused Chunks: {analysis_report['citation_coverage']['unused_count']}\n\n")
                
                if analysis_report['cited_chunks_analysis']['cited_chunks']:
                    f.write("Cited Chunks Details:\n")
                    for j, chunk in enumerate(analysis_report['cited_chunks_analysis']['cited_chunks'], 1):
                        f.write(f"{j}. Source: {chunk['source']}\n")
                        f.write(f"   Chunk Index: {chunk['chunk_index']}\n")
                        f.write(f"   Citation Count: {chunk['citation_count']}\n")
                        f.write(f"   Content Preview: {chunk['text_preview']}\n\n")
            
            results.append(result)
            
            print(f"✅ 测试 {i} 完成")
            print(f"   处理时间: {processing_time:.2f} 秒")
            print(f"   上下文片段: {len(context)} 个")
            print(f"   引用覆盖率: {analysis_report['citation_coverage']['coverage_percentage']}%")
            
        except Exception as e:
            print(f"❌ 测试 {i} 失败: {str(e)}")
            results.append({
                "question_id": i,
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        # 等待2秒
        if i < len(questions):
            print("⏳ 等待2秒后继续...")
            time.sleep(2)
    
    # 保存汇总结果
    successful_tests = [r for r in results if 'error' not in r]
    failed_tests = [r for r in results if 'error' in r]
    
    if successful_tests:
        avg_processing_time = sum(r['processing_time'] for r in successful_tests) / len(successful_tests)
        avg_citation_coverage = sum(r['citation_analysis']['citation_coverage']['coverage_percentage'] for r in successful_tests) / len(successful_tests)
    else:
        avg_processing_time = 0
        avg_citation_coverage = 0
    
    # 保存汇总报告
    summary_file = output_dir / "quick_test_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("快速测试汇总报告\n")
        f.write("="*40 + "\n\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"成功测试: {len(successful_tests)}/3\n")
        f.write(f"失败测试: {len(failed_tests)}/3\n")
        f.write(f"平均处理时间: {avg_processing_time:.2f} 秒\n")
        f.write(f"平均引用覆盖率: {avg_citation_coverage:.2f}%\n\n")
        
        for result in results:
            f.write(f"问题 {result['question_id']}: {result['question']}\n")
            if 'error' in result:
                f.write(f"状态: 失败 - {result['error']}\n")
            else:
                f.write(f"状态: 成功\n")
                f.write(f"处理时间: {result['processing_time']} 秒\n")
                f.write(f"引用覆盖率: {result['citation_analysis']['citation_coverage']['coverage_percentage']}%\n")
            f.write("\n")
    
    print(f"\n🎉 快速测试完成！")
    print(f"📊 成功: {len(successful_tests)}/3")
    print(f"📊 失败: {len(failed_tests)}/3")
    print(f"📊 平均引用覆盖率: {avg_citation_coverage:.2f}%")
    print(f"📁 结果保存在: {output_dir}")


if __name__ == "__main__":
    quick_test() 