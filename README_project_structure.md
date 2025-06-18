# 有机电催化专家系统 - 项目结构

本项目是一个基于深度学习的有机电催化专家系统，包含问答系统、热图可视化和引用分析等功能。

## 📁 项目结构

```
ChemQA/
├── 📁 src/                          # 源代码目录
│   ├── 📁 api_integration/          # API集成模块
│   ├── 📁 knowledge_base/           # 知识库管理
│   ├── 📁 pipeline/                 # 数据处理流程
│   ├── 📁 qa_system/               # 问答系统核心
│   ├── 📁 utils/                   # 工具函数
│   └── 📁 visualization/           # 可视化模块
│
├── 📁 heatmap_visualization/        # 热图可视化模块
│   ├── run_heatmap.py              # 热图生成脚本
│   ├── organic_electrocatalysis_heatmap.png  # 生成的热图
│   ├── README_heatmap.md           # 热图功能说明
│   └── HEATMAP_SUMMARY.md          # 热图功能总结
│
├── 📁 citation_analysis/            # 引用分析模块
│   ├── README_citation_analysis.md  # 引用分析功能说明
│   ├── CITATION_ANALYSIS_SUMMARY.md # 引用分析功能总结
│   └── citation_analysis.txt        # 示例分析结果
│
├── 📁 qa_testing/                   # 问答测试模块
│   ├── demo_qa_test.py             # 演示脚本（模拟数据）
│   ├── quick_test_qa.py            # 快速测试脚本（3个问题）
│   ├── test_organic_electrocatalysis_qa.py  # 完整测试脚本（10个问题）
│   ├── README_qa_testing.md        # 测试功能说明
│   ├── 📁 demo_output/             # 演示输出结果
│   └── 📁 quick_test_output/       # 快速测试输出结果
│
├── 📁 config/                      # 配置文件
├── 📁 data/                        # 数据目录
├── 📁 models/                      # 模型文件
├── 📁 output/                      # 系统输出
├── 📁 examples/                    # 示例文件
├── main.py                         # 主程序入口
├── requirements.txt                # 依赖列表
└── README.md                       # 项目主说明
```

## 🚀 快速开始

### 1. 热图可视化

```bash
cd heatmap_visualization
python3 run_heatmap.py
```

生成有机电催化查询-文本块相似度热图，显示5个关键查询与15个最相关文本块的相关性。

### 2. 引用分析演示

```bash
cd qa_testing
python3 demo_qa_test.py
```

使用模拟数据演示10个有机电催化问题的引用分析功能。

### 3. 问答系统测试

```bash
cd qa_testing
python3 quick_test_qa.py    # 快速测试（3个问题）
# 或
python3 test_organic_electrocatalysis_qa.py  # 完整测试（10个问题）
```

测试问答系统的性能和引用分析能力。

## 📊 功能模块

### 1. 热图可视化 (`heatmap_visualization/`)

**功能特点：**
- 生成查询-文本块相似度热图
- 支持5个关键有机电催化查询
- 显示前15个最相关文本块
- 优化的颜色映射和字体大小
- 适合学术报告和演示

**核心文件：**
- `run_heatmap.py`: 热图生成脚本
- `README_heatmap.md`: 详细使用说明
- `HEATMAP_SUMMARY.md`: 功能总结

### 2. 引用分析 (`citation_analysis/`)

**功能特点：**
- 自动识别多种引用格式
- 统计引用覆盖率和分布
- 生成详细的分析报告
- 支持控制台输出和文件保存
- 集成到专家系统中

**核心文件：**
- `README_citation_analysis.md`: 功能说明
- `CITATION_ANALYSIS_SUMMARY.md`: 功能总结
- `citation_analysis.txt`: 示例分析结果

### 3. 问答测试 (`qa_testing/`)

**功能特点：**
- 10个专业有机电催化问题
- 多种测试模式（演示、快速、完整）
- 自动引用分析
- 详细的测试报告
- 支持JSON和文本格式输出

**核心文件：**
- `demo_qa_test.py`: 演示脚本（模拟数据）
- `quick_test_qa.py`: 快速测试脚本
- `test_organic_electrocatalysis_qa.py`: 完整测试脚本
- `README_qa_testing.md`: 测试功能说明

## 🔧 技术栈

- **Python 3.8+**: 主要开发语言
- **DeepSeek API**: AI问答接口
- **sentence-transformers**: 文本向量化
- **matplotlib/seaborn**: 数据可视化
- **numpy**: 数值计算
- **pandas**: 数据处理

## 📈 性能指标

### 热图可视化
- **处理时间**: ~15秒（5个查询×1785个文档）
- **输出质量**: 531KB高分辨率图像
- **颜色优化**: 0.4-0.8相似度范围

### 引用分析
- **识别准确率**: 支持多种引用格式
- **分析速度**: 毫秒级处理
- **覆盖率统计**: 精确的引用分布分析

### 问答测试
- **平均引用覆盖率**: 74.00%（演示数据）
- **处理时间**: 秒级响应
- **成功率**: 100%（演示测试）

## 📝 使用说明

### 开发环境设置

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置API密钥**
在 `config/settings.py` 中配置DeepSeek API密钥

3. **初始化知识库**
确保知识库已正确初始化并包含相关文献

### 运行测试

1. **热图生成**
```bash
cd heatmap_visualization
python3 run_heatmap.py
```

2. **引用分析演示**
```bash
cd qa_testing
python3 demo_qa_test.py
```

3. **问答系统测试**
```bash
cd qa_testing
python3 quick_test_qa.py
```

## 📊 输出示例

### 热图可视化
- 生成 `organic_electrocatalysis_heatmap.png`
- 显示查询-文本块相似度矩阵
- 优化的颜色映射和标签

### 引用分析
- 详细的引用覆盖率统计
- 被引用片段信息
- 未使用片段分析

### 问答测试
- 每个问题的答案文件
- 引用分析报告
- 汇总统计信息

## 🔍 故障排除

### 常见问题

1. **路径问题**
   - 确保在正确的目录中运行脚本
   - 检查Python路径配置

2. **依赖问题**
   - 确保所有依赖包已安装
   - 检查Python版本兼容性

3. **API问题**
   - 验证API密钥配置
   - 检查网络连接和API配额

### 调试模式

启用详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 文档说明

- **README.md**: 项目主说明
- **各模块README**: 详细功能说明
- **SUMMARY文档**: 功能总结和示例
- **代码注释**: 详细的代码说明

## 🤝 贡献指南

1. 遵循现有的代码结构
2. 添加适当的文档说明
3. 包含测试用例
4. 更新相关README文件

这个项目结构清晰地组织了不同功能模块，便于维护和使用。每个模块都有独立的文档说明，方便用户快速上手和深入使用。 