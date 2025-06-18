# ChemQA - 有机电催化智能问答系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

ChemQA是一个基于深度学习的智能问答系统，专门用于有机电催化领域的学术研究。系统通过处理大量科学文献，为用户提供专业、准确的有机电催化相关问题解答。

## 🌟 主要特性

- **专业领域聚焦**: 专注于有机电催化、电化学合成和催化转化领域
- **智能文献检索**: 基于向量相似度的精准文献检索系统
- **AI驱动回答**: 集成DeepSeek API，生成专业、结构化的学术回答
- **引用分析**: 自动分析答案的文献引用情况，确保学术严谨性
- **可视化分析**: 提供查询-文档相似度热力图，直观展示检索效果
- **批量测试**: 支持批量问题测试和答案质量评估

## 🏗️ 系统架构

```
ChemQA/
├── config/                 # 配置文件
│   ├── settings.py        # 系统设置
│   └── prompts.py         # AI提示模板
├── data/                  # 数据目录
│   ├── raw_papers/        # 原始PDF文献
│   ├── processed/         # 处理后的文本块
│   └── vector_db/         # 向量数据库
├── models/                
│   └── text2vec/         # 文本向量化模型
├── src/                   # 源代码
│   ├── api_integration/   # API集成模块
│   ├── knowledge_base/    # 知识库管理
│   ├── pipeline/          # 数据处理管道
│   ├── qa_system/         # 问答系统核心
│   ├── utils/             # 工具函数
│   └── visualization/     # 可视化模块
├── qa_testing/           # 测试模块
├── heatmap_visualization/ # 热力图可视化
└── output/               # 输出结果
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 8GB+ RAM (推荐16GB)
- 足够的磁盘空间存储文献和向量数据

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/Chraise/ChemQA.git
cd ChemQA
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置API密钥**
编辑 `config/settings.py` 文件，设置您的DeepSeek API密钥：
```python
DEEPSEEK_API_CONFIG = {
    "api_key": "your-api-key-here",
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-reasoner",
    "temperature": 0.3
}
```

4. **构建知识库**
```bash
python src/pipeline/vector_index_builder.py
```

### 使用方法，注：DeepSeek API 有一定几率出现服务器繁忙，需要再次尝试！

#### 命令行模式
```bash
# 单次问答
python main.py -q "What are the key mechanisms of CO2 electroreduction on copper-based catalysts?"

# 交互模式
python main.py
```

#### 批量测试
```bash
# 运行预设的测试问题
python qa_testing/test_organic_electrocatalysis_qa.py
```

#### 生成热力图
```bash
# 生成查询-文档相似度热力图
python heatmap_visualization/run_heatmap.py
```

## 📚 核心模块说明

### 1. 知识库管理 (`src/knowledge_base/`)
- **PDF加载器**: 支持批量PDF文献解析
- **文本处理器**: 智能文本分块和预处理
- **向量存储**: 基于FAISS的高效向量检索
- **检索器**: 语义相似度搜索

### 2. 问答系统 (`src/qa_system/`)
- **专家系统**: 核心问答逻辑
- **回答生成器**: 基于DeepSeek API的专业回答生成
- **引用分析器**: 自动分析答案的文献引用
- **响应格式化器**: 结构化输出格式化

### 3. API集成 (`src/api_integration/`)
- **API处理器**: DeepSeek API调用封装
- **回答生成器**: 提示工程和回答生成

### 4. 可视化 (`src/visualization/`)
- **热力图生成器**: 查询-文档相似度可视化
- **相似度分析**: 检索效果评估

## 🔧 配置说明

### 主要配置参数 (`config/settings.py`)

```python
# 文本处理参数
CHUNK_SIZE = 500          # 文本块大小
CHUNK_OVERLAP = 50        # 文本块重叠

# 向量检索配置
RETRIEVAL_TOP_K = 10      # 检索文档数量
EMBEDDING_MODEL = "text2vec/paraphrase-multilingual-MiniLM-L12-v2"

# API配置
DEEPSEEK_API_CONFIG = {
    "model": "deepseek-reasoner",
    "temperature": 0.3
}
```

### 提示模板 (`config/prompts.py`)

系统使用结构化的提示模板，确保生成的回答包含：
- 回答摘要
- 技术细节
- 实际应用
- 局限性分析

## 📊 输出格式

系统生成的回答采用Markdown格式，包含以下结构：

```markdown
# 问题分析

## 回答摘要
[关键发现和结论]

## 技术细节
[详细的技术分析]

## 实际应用
[工业应用前景]

## 局限性/研究空白
[当前研究的不足]

## 参考文献
[引用的文献列表]
```
