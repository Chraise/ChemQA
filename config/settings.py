# 主配置文件

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings:
    # 数据路径
    RAW_PAPERS_DIR = os.path.join(BASE_DIR, "data", "raw_papers")
    PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
    VECTOR_DB_DIR = os.path.join(BASE_DIR, "data", "vector_db")

    # 文本处理参数
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

    # 向量存储配置
    EMBEDDING_MODEL = "text2vec/paraphrase-multilingual-MiniLM-L12-v2"  # 使用本地模型
    RETRIEVAL_TOP_K = 10  # 增加检索文档数量

    # 更新为DeepSeek API配置
    DEEPSEEK_API_CONFIG = {
        "api_key": "sk-0a6b9d29efa94458ad99009fcb5b46bb",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-reasoner",
        "temperature": 0.3
    }

    # PDF解析设置
    PDF_PARSING_ENGINE = "pymupdf"

    # 系统配置保持不变
    DOMAIN = "organic electrocatalysis"
    MAX_TOKENS = 30000

    MODEL_DIR = os.path.join(BASE_DIR, "models")  # 模型存储根目录

settings = Settings()
