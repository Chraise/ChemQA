import json
import os
from typing import List, Dict, Any

import numpy as np
from sentence_transformers import SentenceTransformer

from config.settings import settings
from src.knowledge_base.pdf_loader import PDFLoader
from src.utils.logger import logger


class VectorStore:
    def __init__(self):
        """初始化向量存储"""
        self.model = self._load_model()
        self.vector_index = self._load_vector_index()
        logger.info("Vector store initialized successfully")

    def _load_model(self) -> SentenceTransformer:
        """加载文本向量化模型"""
        try:
            # 使用预训练模型名称或本地模型路径
            model_name = settings.EMBEDDING_MODEL
            logger.info(f"Loading model: {model_name}")

            # 如果是本地模型路径，使用完整路径
            if os.path.exists(os.path.join(settings.MODEL_DIR, model_name)):
                model_path = os.path.join(settings.MODEL_DIR, model_name)
                logger.info(f"Using local model from {model_path}")
                model = SentenceTransformer(model_path)
            else:
                # 否则使用预训练模型名称
                logger.info(f"Using pretrained model: {model_name}")
                model = SentenceTransformer(model_name)
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def _convert_index_format(self, old_index):
        """将旧的向量索引格式转换为新格式"""
        documents = []
        vectors = []

        # 使用正确的路径
        pdf_loader = PDFLoader(settings.RAW_PAPERS_DIR)

        for file_path, vector in old_index.items():
            try:
                # 从文件路径中提取源文件和块索引
                base_path = file_path.rsplit('_', 1)[0]  # 移除块索引后缀
                chunk_index = int(file_path.rsplit('_', 1)[1])

                # 加载PDF文件
                pdf_results = pdf_loader.load_pdf(base_path)
                if not pdf_results:
                    logger.warning(f"No content found in {base_path}")
                    continue

                # 获取文本内容
                text = pdf_results[0].get('text', '')
                if not text:
                    logger.warning(f"No text content in {base_path}")
                    continue

                # 创建文档对象
                doc = {
                    'text': text,
                    'metadata': {
                        'source': base_path,
                        'chunk_index': chunk_index
                    }
                }

                documents.append(doc)
                vectors.append(vector)

            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                continue

        return {
            'documents': documents,
            'vectors': vectors
        }

    def _load_vector_index(self) -> Dict[str, Any]:
        """加载向量索引"""
        try:
            index_path = os.path.join(settings.VECTOR_DB_DIR, "vector_index.json")
            logger.info(f"Loading vector index from {index_path}")

            if not os.path.exists(index_path):
                logger.warning(f"Vector index not found at {index_path}")
                return {"documents": [], "vectors": []}

            with open(index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查数据格式并转换
            if "documents" not in data or "vectors" not in data:
                logger.info("Converting vector index to new format...")
                data = self._convert_index_format(data)
                # 保存转换后的格式
                self._save_vector_index(data)

            # 确保向量是numpy数组
            if isinstance(data["vectors"], list):
                data["vectors"] = np.array(data["vectors"])

            return data
        except Exception as e:
            logger.error(f"Error loading vector index: {str(e)}")
            raise

    def _save_vector_index(self, data: Dict[str, Any] = None):
        """保存向量索引到文件"""
        try:
            index_path = os.path.join(settings.VECTOR_DB_DIR, "vector_index.json")

            # 如果没有提供数据，使用当前索引
            if data is None:
                data = self.vector_index

            # 将numpy数组转换为列表以便JSON序列化
            save_data = {
                "documents": data["documents"],
                "vectors": data["vectors"].tolist()
            }

            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Vector index saved to {index_path}")

        except Exception as e:
            logger.error(f"Error saving vector index: {str(e)}")
            raise

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        执行相似度搜索
        
        Args:
            query: 查询文本
            top_k: 返回的最相关文档数量
            
        Returns:
            包含文档和相似度分数的列表，每个元素格式为:
            {
                "document": {
                    "text": str,
                    "source": str,
                    "chunk_index": int
                },
                "score": float
            }
        """
        try:
            # 如果没有文档，返回空列表
            if not self.vector_index.get("documents"):
                logger.warning("No documents in vector store")
                return []

            # 将查询转换为向量
            query_vector = self.model.encode(query)

            # 计算相似度分数 - 使用点积作为相似度度量
            scores = np.dot(self.vector_index["vectors"], query_vector)

            # 获取前K个最相似的文档
            top_indices = np.argsort(scores)[-top_k:][::-1]
            top_scores = scores[top_indices]

            # 构建标准化的结果
            results = []
            for idx, score in zip(top_indices, top_scores):
                doc = self.vector_index["documents"][idx]
                # 确保文档格式符合预期
                result = {
                    "document": {
                        "text": doc.get("text", ""),
                        "source": doc.get("source", ""),
                        "chunk_index": doc.get("chunk_index", -1)
                    },
                    "score": float(score)
                }
                results.append(result)

            logger.info(f"Found {len(results)} relevant documents for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        添加文档到向量存储
        
        Args:
            documents: 文档列表，每个文档必须包含text字段，可选包含source和chunk_index字段
        """
        try:
            # 标准化文档格式
            normalized_docs = []
            texts = []

            for doc in documents:
                # 提取文本内容
                if "text" in doc:
                    text = doc["text"]
                elif "metadata" in doc and "text" in doc["metadata"]:
                    text = doc["metadata"]["text"]
                else:
                    raise ValueError("Document must contain 'text' field")

                # 创建标准化文档
                normalized_doc = {
                    "text": text,
                    "source": doc.get("source", ""),
                    "chunk_index": doc.get("chunk_index", -1)
                }

                normalized_docs.append(normalized_doc)
                texts.append(text)

            # 生成向量
            vectors = self.model.encode(texts)

            # 更新索引
            if not self.vector_index.get("documents"):
                self.vector_index["documents"] = []
                self.vector_index["vectors"] = np.array([])

            self.vector_index["documents"].extend(normalized_docs)
            if len(self.vector_index["vectors"]) == 0:
                self.vector_index["vectors"] = vectors
            else:
                self.vector_index["vectors"] = np.vstack([self.vector_index["vectors"], vectors])

            # 保存更新后的索引
            self._save_vector_index()

            logger.info(f"Added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
