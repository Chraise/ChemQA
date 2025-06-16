# Organic Electrocatalysis Expert System

这是一个基于深度学习的有机电催化专家系统，能够回答与有机电催化相关的问题，并提供专业的分析和建议。

## 功能特点

- 基于 DeepSeek API 的智能问答系统
- 支持 PDF 文献的自动解析和知识提取
- 向量化存储和检索相关文献内容
- 专业的电催化领域知识库
- 支持中文和英文问答

## 系统要求

- Python 3.8+
- 操作系统：Linux/macOS/Windows

## 项目结构

```
ChemQA/
├── config/                 # 配置文件
│   ├── prompts.py         # 提示词模板
│   └── settings.py        # 系统设置
├── data/                  # 数据目录
│   ├── raw_papers/       # 原始文献
│   ├── processed/        # 处理后的数据
│   └── vector_db/        # 向量数据库
├── models/               # 模型文件
│   └── text2vec/        # 文本向量化模型
├── src/                 # 源代码
│   ├── api_integration/ # API 集成
│   ├── knowledge_base/  # 知识库
│   ├── pipeline/        # 数据处理流程
│   ├── qa_system/       # 问答系统
│   └── utils/           # 工具函数
├── output/              # 输出目录
├── main.py             # 主程序
└── requirements.txt    # 依赖列表
```

## 主要模块说明

- `api_integration/`: DeepSeek API 的集成模块
- `knowledge_base/`: 文献处理和知识库管理
- `pipeline/`: 数据处理和向量索引构建
- `qa_system/`: 核心问答系统
- `utils/`: 通用工具函数

## 配置说明

主要配置项在 `config/settings.py` 中：

- `RETRIEVAL_TOP_K`: 检索相关文档数量
- `CHUNK_SIZE`: 文本分块大小
- `CHUNK_OVERLAP`: 文本分块重叠大小
- `VECTOR_DB_PATH`: 向量数据库路径

## 注意事项

1. 首次运行前请确保已正确配置 API 密钥
2. 建议定期更新知识库以保持信息的时效性
3. 处理大量文献时请确保有足够的磁盘空间
