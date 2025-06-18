#!/usr/bin/env python3
"""
对比分析脚本

比较有无本地文献库检索功能的差异，分析两种方法的优缺点。
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from citation_analysis.citation_analyzer import CitationAnalyzer


class ComparisonAnalyzer:
    """对比分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.citation_analyzer = CitationAnalyzer()
        
        # 定义输出目录
        self.output_dir = Path("comparison_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # 定义输入目录
        self.retrieval_dir = Path("qa_testing_output")  # 有文献库检索的结果
        self.direct_api_dir = Path("direct_api_output")  # 直接API的结果
        
        # 存储对比数据
        self.comparison_data = []
    
    def load_test_results(self, directory: Path) -> dict:
        """加载测试结果"""
        summary_file = directory / "summary.json"
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def load_direct_api_results(self) -> dict:
        """加载直接API结果"""
        summary_file = self.direct_api_dir / "direct_api_summary.json"
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def analyze_citations(self, answer_file: Path) -> dict:
        """分析引用情况"""
        try:
            with open(answer_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取答案部分（去掉markdown格式）
            if content.startswith('#'):
                # 找到第一个空行后的内容
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == '' and i > 0:
                        answer = '\n'.join(lines[i+1:])
                        break
                else:
                    answer = content
            else:
                answer = content
            
            # 分析引用
            analysis = self.citation_analyzer.analyze_citations(answer)
            return analysis
        except Exception as e:
            print(f"分析引用失败 {answer_file}: {str(e)}")
            return {"citation_count": 0, "context_fragments": 0}
    
    def compare_methods(self):
        """对比两种方法"""
        print("🔍 开始对比分析...")
        
        # 加载结果
        retrieval_results = self.load_test_results(self.retrieval_dir)
        direct_api_results = self.load_direct_api_results()
        
        if not retrieval_results or not direct_api_results:
            print("❌ 无法加载测试结果，请确保两种方法都已运行完成")
            return
        
        print("✅ 成功加载两种方法的测试结果")
        
        # 分析每个问题的对比
        for i in range(1, 11):  # 10个问题
            print(f"\n分析问题 {i}...")
            
            # 加载两种方法的答案
            retrieval_answer_file = self.retrieval_dir / f"answer_{i:02d}.md"
            direct_answer_file = self.direct_api_dir / f"direct_answer_{i:02d}.md"
            
            if not retrieval_answer_file.exists() or not direct_answer_file.exists():
                print(f"⚠️  问题 {i} 的答案文件不完整，跳过")
                continue
            
            # 分析引用情况
            retrieval_citations = self.analyze_citations(retrieval_answer_file)
            direct_citations = self.analyze_citations(direct_answer_file)
            
            # 获取处理时间
            retrieval_time = 0
            direct_time = 0
            
            for result in retrieval_results.get("detailed_results", []):
                if result.get("question_id") == i:
                    retrieval_time = result.get("processing_time", 0)
                    break
            
            for result in direct_api_results.get("detailed_results", []):
                if result.get("question_id") == i:
                    direct_time = result.get("processing_time", 0)
                    break
            
            # 计算答案长度
            with open(retrieval_answer_file, 'r', encoding='utf-8') as f:
                retrieval_length = len(f.read())
            
            with open(direct_answer_file, 'r', encoding='utf-8') as f:
                direct_length = len(f.read())
            
            # 存储对比数据
            comparison_item = {
                "question_id": i,
                "retrieval": {
                    "processing_time": retrieval_time,
                    "answer_length": retrieval_length,
                    "citation_count": retrieval_citations.get("citation_count", 0),
                    "context_fragments": retrieval_citations.get("context_fragments", 0)
                },
                "direct_api": {
                    "processing_time": direct_time,
                    "answer_length": direct_length,
                    "citation_count": direct_citations.get("citation_count", 0),
                    "context_fragments": direct_citations.get("context_fragments", 0)
                }
            }
            
            self.comparison_data.append(comparison_item)
        
        # 生成对比报告
        self.generate_comparison_report()
        
        # 生成可视化图表
        self.generate_comparison_charts()
        
        print(f"\n🎉 对比分析完成！结果保存在: {self.output_dir}")
    
    def generate_comparison_report(self):
        """生成对比报告"""
        if not self.comparison_data:
            print("❌ 没有对比数据可生成报告")
            return
        
        # 计算统计信息
        retrieval_times = [item["retrieval"]["processing_time"] for item in self.comparison_data]
        direct_times = [item["direct_api"]["processing_time"] for item in self.comparison_data]
        
        retrieval_lengths = [item["retrieval"]["answer_length"] for item in self.comparison_data]
        direct_lengths = [item["direct_api"]["answer_length"] for item in self.comparison_data]
        
        retrieval_citations = [item["retrieval"]["citation_count"] for item in self.comparison_data]
        direct_citations = [item["direct_api"]["citation_count"] for item in self.comparison_data]
        
        retrieval_fragments = [item["retrieval"]["context_fragments"] for item in self.comparison_data]
        direct_fragments = [item["direct_api"]["context_fragments"] for item in self.comparison_data]
        
        # 生成报告
        report_file = self.output_dir / "comparison_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("有无文献库检索功能对比分析报告\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"对比问题数: {len(self.comparison_data)}\n\n")
            
            f.write("1. 处理时间对比\n")
            f.write("-" * 30 + "\n")
            f.write(f"文献库检索平均时间: {sum(retrieval_times)/len(retrieval_times):.2f} 秒\n")
            f.write(f"直接API平均时间: {sum(direct_times)/len(direct_times):.2f} 秒\n")
            f.write(f"时间差异: {sum(retrieval_times)/len(retrieval_times) - sum(direct_times)/len(direct_times):.2f} 秒\n\n")
            
            f.write("2. 答案长度对比\n")
            f.write("-" * 30 + "\n")
            f.write(f"文献库检索平均长度: {sum(retrieval_lengths)/len(retrieval_lengths):.0f} 字符\n")
            f.write(f"直接API平均长度: {sum(direct_lengths)/len(direct_lengths):.0f} 字符\n")
            f.write(f"长度差异: {sum(retrieval_lengths)/len(retrieval_lengths) - sum(direct_lengths)/len(direct_lengths):.0f} 字符\n\n")
            
            f.write("3. 引用数量对比\n")
            f.write("-" * 30 + "\n")
            f.write(f"文献库检索平均引用: {sum(retrieval_citations)/len(retrieval_citations):.1f} 个\n")
            f.write(f"直接API平均引用: {sum(direct_citations)/len(direct_citations):.1f} 个\n")
            f.write(f"引用差异: {sum(retrieval_citations)/len(retrieval_citations) - sum(direct_citations)/len(direct_citations):.1f} 个\n\n")
            
            f.write("4. 上下文片段对比\n")
            f.write("-" * 30 + "\n")
            f.write(f"文献库检索平均片段: {sum(retrieval_fragments)/len(retrieval_fragments):.1f} 个\n")
            f.write(f"直接API平均片段: {sum(direct_fragments)/len(direct_fragments):.1f} 个\n")
            f.write(f"片段差异: {sum(retrieval_fragments)/len(retrieval_fragments) - sum(direct_fragments)/len(direct_fragments):.1f} 个\n\n")
            
            f.write("5. 详细对比数据\n")
            f.write("-" * 30 + "\n")
            for item in self.comparison_data:
                f.write(f"\n问题 {item['question_id']}:\n")
                f.write(f"  文献库检索: {item['retrieval']['processing_time']:.2f}s, "
                       f"{item['retrieval']['answer_length']}字符, "
                       f"{item['retrieval']['citation_count']}引用, "
                       f"{item['retrieval']['context_fragments']}片段\n")
                f.write(f"  直接API: {item['direct_api']['processing_time']:.2f}s, "
                       f"{item['direct_api']['answer_length']}字符, "
                       f"{item['direct_api']['citation_count']}引用, "
                       f"{item['direct_api']['context_fragments']}片段\n")
        
        # 保存JSON格式的对比数据
        json_file = self.output_dir / "comparison_data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.comparison_data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 对比报告已生成: {report_file}")
    
    def generate_comparison_charts(self):
        """生成对比图表"""
        if not self.comparison_data:
            print("❌ 没有对比数据可生成图表")
            return
        
        # 设置图表样式
        plt.style.use('default')
        sns.set_palette("husl")
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('有无文献库检索功能对比分析', fontsize=16, fontweight='bold')
        
        # 准备数据
        questions = [f"Q{i}" for i in range(1, len(self.comparison_data) + 1)]
        retrieval_times = [item["retrieval"]["processing_time"] for item in self.comparison_data]
        direct_times = [item["direct_api"]["processing_time"] for item in self.comparison_data]
        
        retrieval_lengths = [item["retrieval"]["answer_length"] for item in self.comparison_data]
        direct_lengths = [item["direct_api"]["answer_length"] for item in self.comparison_data]
        
        retrieval_citations = [item["retrieval"]["citation_count"] for item in self.comparison_data]
        direct_citations = [item["direct_api"]["citation_count"] for item in self.comparison_data]
        
        retrieval_fragments = [item["retrieval"]["context_fragments"] for item in self.comparison_data]
        direct_fragments = [item["direct_api"]["context_fragments"] for item in self.comparison_data]
        
        # 1. 处理时间对比
        x = range(len(questions))
        width = 0.35
        
        axes[0, 0].bar([i - width/2 for i in x], retrieval_times, width, label='文献库检索', alpha=0.8)
        axes[0, 0].bar([i + width/2 for i in x], direct_times, width, label='直接API', alpha=0.8)
        axes[0, 0].set_xlabel('问题编号')
        axes[0, 0].set_ylabel('处理时间 (秒)')
        axes[0, 0].set_title('处理时间对比')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(questions)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 答案长度对比
        axes[0, 1].bar([i - width/2 for i in x], retrieval_lengths, width, label='文献库检索', alpha=0.8)
        axes[0, 1].bar([i + width/2 for i in x], direct_lengths, width, label='直接API', alpha=0.8)
        axes[0, 1].set_xlabel('问题编号')
        axes[0, 1].set_ylabel('答案长度 (字符)')
        axes[0, 1].set_title('答案长度对比')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(questions)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 引用数量对比
        axes[1, 0].bar([i - width/2 for i in x], retrieval_citations, width, label='文献库检索', alpha=0.8)
        axes[1, 0].bar([i + width/2 for i in x], direct_citations, width, label='直接API', alpha=0.8)
        axes[1, 0].set_xlabel('问题编号')
        axes[1, 0].set_ylabel('引用数量')
        axes[1, 0].set_title('引用数量对比')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(questions)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 上下文片段对比
        axes[1, 1].bar([i - width/2 for i in x], retrieval_fragments, width, label='文献库检索', alpha=0.8)
        axes[1, 1].bar([i + width/2 for i in x], direct_fragments, width, label='直接API', alpha=0.8)
        axes[1, 1].set_xlabel('问题编号')
        axes[1, 1].set_ylabel('上下文片段数量')
        axes[1, 1].set_title('上下文片段对比')
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(questions)
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 保存图表
        chart_file = self.output_dir / "comparison_charts.png"
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 对比图表已生成: {chart_file}")


def main():
    """主函数"""
    print("📊 对比分析脚本")
    print("="*60)
    print("🔍 比较有无本地文献库检索功能的差异")
    
    # 创建分析器并运行对比
    analyzer = ComparisonAnalyzer()
    analyzer.compare_methods()


if __name__ == "__main__":
    main() 