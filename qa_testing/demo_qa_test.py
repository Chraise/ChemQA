#!/usr/bin/env python3
"""
有机电催化问答测试演示脚本

使用模拟数据演示10个英文有机电催化问题的引用分析功能。
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.qa_system.citation_analyzer import analyze_answer_citations


def create_mock_data():
    """创建模拟的问答数据"""
    
    # 10个有机电催化领域的问题
    questions = [
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
    
    # 模拟的上下文片段（每个问题对应不同的片段）
    mock_contexts = []
    
    for i in range(10):
        context = [
            {
                "source": f"paper_{i+1}_A.pdf",
                "chunk_index": 1,
                "text": f"Research on {questions[i].lower().split()[0]} mechanisms has shown significant progress in recent years. The key factors include catalyst structure, reaction conditions, and electrolyte composition."
            },
            {
                "source": f"paper_{i+1}_B.pdf",
                "chunk_index": 2,
                "text": f"Electrochemical studies reveal that the coordination environment plays a crucial role in determining catalytic activity and selectivity for organic transformations."
            },
            {
                "source": f"paper_{i+1}_C.pdf",
                "chunk_index": 3,
                "text": f"Advanced characterization techniques such as in-situ spectroscopy and microscopy provide insights into the reaction mechanisms and catalyst evolution."
            },
            {
                "source": f"paper_{i+1}_D.pdf",
                "chunk_index": 4,
                "text": f"The development of novel catalyst materials and optimization of reaction conditions have led to improved performance and selectivity in organic electrocatalysis."
            },
            {
                "source": f"paper_{i+1}_E.pdf",
                "chunk_index": 5,
                "text": f"Understanding the structure-activity relationships is essential for designing efficient electrocatalysts for organic synthesis applications."
            }
        ]
        mock_contexts.append(context)
    
    # 模拟的答案（包含不同程度的引用）
    mock_answers = [
        # 问题1：100%引用覆盖率
        """CO2 electroreduction mechanisms on copper-based catalysts involve multiple pathways [Ref 1]. The coordination environment significantly influences catalytic performance [Ref 2]. Advanced characterization techniques reveal key intermediates [Ref 3]. Novel catalyst materials show improved selectivity [Ref 4]. Structure-activity relationships guide catalyst design [Ref 5].""",
        
        # 问题2：80%引用覆盖率
        """The coordination environment affects nickel-based electrocatalyst performance through electronic and geometric effects [Ref 2]. Recent studies show that catalyst structure determines activity [Ref 1]. In-situ characterization provides mechanistic insights [Ref 3]. Optimization of reaction conditions improves selectivity [Ref 4].""",
        
        # 问题3：60%引用覆盖率
        """Electrochemical C-H functionalization has advanced significantly with new catalyst designs [Ref 1]. The coordination environment plays a key role [Ref 2]. Advanced techniques reveal reaction mechanisms [Ref 3].""",
        
        # 问题4：40%引用覆盖率
        """Selectivity improvement in carbonyl reduction requires understanding catalyst structure [Ref 1]. The coordination environment influences performance [Ref 2].""",
        
        # 问题5：100%引用覆盖率
        """Electrolyte additives play crucial roles in organic electrocatalysis [Ref 1]. They affect the coordination environment and catalytic performance [Ref 2]. Advanced characterization reveals their effects [Ref 3]. Novel materials show improved performance [Ref 4]. Structure-activity relationships guide optimization [Ref 5].""",
        
        # 问题6：80%引用覆盖率
        """Platinum catalyst surface structure influences organic molecule oxidation through geometric and electronic effects [Ref 1]. The coordination environment determines activity [Ref 2]. In-situ studies reveal mechanistic details [Ref 3]. Novel materials show enhanced performance [Ref 4].""",
        
        # 问题7：60%引用覆盖率
        """Electrochemical synthesis of heterocyclic compounds faces challenges in selectivity and efficiency [Ref 1]. The coordination environment affects performance [Ref 2]. Advanced characterization provides insights [Ref 3].""",
        
        # 问题8：40%引用覆盖率
        """High current density in organic electrosynthesis requires optimized catalyst structure [Ref 1]. The coordination environment influences performance [Ref 2].""",
        
        # 问题9：100%引用覆盖率
        """Biomass-derived compound oxidation mechanisms involve complex reaction pathways [Ref 1]. The coordination environment affects catalytic activity [Ref 2]. Advanced techniques reveal key intermediates [Ref 3]. Novel materials improve performance [Ref 4]. Structure-activity relationships guide design [Ref 5].""",
        
        # 问题10：80%引用覆盖率
        """Electrolyte pH significantly affects reaction pathways in organic electrocatalysis [Ref 1]. The coordination environment changes with pH [Ref 2]. In-situ studies show pH-dependent mechanisms [Ref 3]. Novel materials show pH-dependent performance [Ref 4]."""
    ]
    
    return questions, mock_contexts, mock_answers


def run_demo():
    """运行演示"""
    
    # 创建输出目录
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    
    print("🧪 有机电催化问答测试演示")
    print("="*60)
    print("📝 使用模拟数据演示10个问题的引用分析")
    print(f"📁 输出目录: {output_dir}")
    
    # 获取模拟数据
    questions, contexts, answers = create_mock_data()
    
    results = []
    
    for i in range(10):
        print(f"\n{'='*60}")
        print(f"演示 {i+1}/10: {questions[i]}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            
            # 分析引用情况
            analysis_report = analyze_answer_citations(
                answer=answers[i],
                context=contexts[i],
                print_report=False,
                save_to_file=False
            )
            
            processing_time = time.time() - start_time
            
            # 保存结果
            result = {
                "question_id": i + 1,
                "question": questions[i],
                "processing_time": round(processing_time, 3),
                "timestamp": datetime.now().isoformat(),
                "citation_analysis": analysis_report,
                "context_count": len(contexts[i]),
                "answer_length": len(answers[i]),
                "answer": answers[i]
            }
            
            # 保存答案文件
            answer_file = output_dir / f"answer_{i+1:02d}.md"
            with open(answer_file, 'w', encoding='utf-8') as f:
                f.write(f"# Question {i+1}\n\n")
                f.write(f"**Question:** {questions[i]}\n\n")
                f.write(f"**Answer:**\n{answers[i]}\n\n")
                f.write(f"**Analysis:**\n")
                f.write(f"- Context Chunks: {len(contexts[i])}\n")
                f.write(f"- Citation Coverage: {analysis_report['citation_coverage']['coverage_percentage']}%\n")
                f.write(f"- Cited Chunks: {analysis_report['citation_coverage']['cited_count']}\n")
                f.write(f"- Unused Chunks: {analysis_report['citation_coverage']['unused_count']}\n")
            
            # 保存引用分析
            analysis_file = output_dir / f"citation_analysis_{i+1:02d}.txt"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write(f"Question {i+1}: {questions[i]}\n")
                f.write("="*50 + "\n\n")
                f.write(f"Processing Time: {processing_time:.3f} seconds\n")
                f.write(f"Context Chunks: {len(contexts[i])}\n")
                f.write(f"Answer Length: {len(answers[i])} characters\n\n")
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
            
            print(f"✅ 演示 {i+1} 完成")
            print(f"   处理时间: {processing_time:.3f} 秒")
            print(f"   上下文片段: {len(contexts[i])} 个")
            print(f"   引用覆盖率: {analysis_report['citation_coverage']['coverage_percentage']}%")
            
        except Exception as e:
            print(f"❌ 演示 {i+1} 失败: {str(e)}")
            results.append({
                "question_id": i + 1,
                "question": questions[i],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
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
    summary_file = output_dir / "demo_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("演示测试汇总报告\n")
        f.write("="*40 + "\n\n")
        f.write(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"成功演示: {len(successful_tests)}/10\n")
        f.write(f"失败演示: {len(failed_tests)}/10\n")
        f.write(f"平均处理时间: {avg_processing_time:.3f} 秒\n")
        f.write(f"平均引用覆盖率: {avg_citation_coverage:.2f}%\n\n")
        
        f.write("详细结果:\n")
        for result in results:
            f.write(f"\n问题 {result['question_id']}: {result['question']}\n")
            if 'error' in result:
                f.write(f"状态: 失败 - {result['error']}\n")
            else:
                f.write(f"状态: 成功\n")
                f.write(f"处理时间: {result['processing_time']} 秒\n")
                f.write(f"引用覆盖率: {result['citation_analysis']['citation_coverage']['coverage_percentage']}%\n")
                f.write(f"答案长度: {result['answer_length']} 字符\n")
    
    # 保存JSON格式的详细结果
    json_file = output_dir / "demo_results.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 演示完成！")
    print(f"📊 成功: {len(successful_tests)}/10")
    print(f"📊 失败: {len(failed_tests)}/10")
    print(f"📊 平均引用覆盖率: {avg_citation_coverage:.2f}%")
    print(f"📁 结果保存在: {output_dir}")
    
    # 显示覆盖率分布
    if successful_tests:
        coverages = [r['citation_analysis']['citation_coverage']['coverage_percentage'] for r in successful_tests]
        print(f"\n📈 引用覆盖率分布:")
        print(f"   100%: {coverages.count(100)} 个问题")
        print(f"   80%: {coverages.count(80)} 个问题")
        print(f"   60%: {coverages.count(60)} 个问题")
        print(f"   40%: {coverages.count(40)} 个问题")


if __name__ == "__main__":
    run_demo() 