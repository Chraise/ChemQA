from typing import List, Dict, Any, Optional
from src.knowledge_base.vector_store import VectorStore
from src.utils.logger import logger


class Retriever:
    def __init__(self):
        """初始化检索器"""
        try:
            self.vector_store = VectorStore()
            logger.info("Retriever initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Retriever: {str(e)}")
            raise

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        搜索与查询相关的文档

        Args:
            query: 查询文本
            top_k: 返回的最相关文档数量

        Returns:
            包含相关文档和相似度分数的列表
        """
        try:
            logger.info(f"Searching for query: {query}")
            results = self.vector_store.similarity_search(query, top_k)
            logger.info(f"Found {len(results)} relevant documents")
            return results
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            raise

    def retrieve_relevant_context(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.5,
        return_dict_list: bool = False
    ):
        """
        检索与查询相关的上下文
        Args:
            query: 查询文本
            top_k: 返回的最相关文档数量
            min_score: 最小相似度分数阈值
            return_dict_list: 是否返回文献分块字典列表
        Returns:
            合并后的相关上下文文本，或文献分块字典列表
        """
        try:
            # 搜索相关文档
            results = self.search(query, top_k)

            if not results:
                logger.warning("No relevant documents found")
                return [] if return_dict_list else None

            # 过滤掉相似度分数低于阈值的文档
            filtered_results = [r for r in results if r["score"] >= min_score]

            if not filtered_results:
                logger.warning(f"No documents found with similarity score >= {min_score}")
                return [] if return_dict_list else None

            if return_dict_list:
                # 返回文献分块字典列表
                return [r["document"] for r in filtered_results]

            # 提取文档内容并合并
            contexts = []
            for result in filtered_results:
                doc = result["document"]
                score = result["score"]
                if isinstance(doc, dict) and "metadata" in doc:
                    metadata = doc["metadata"]
                    text = doc.get("text", "")
                    source = metadata.get("source", "")
                    if source:
                        # 添加引用标记
                        text = f"[Ref {source}]\n{text}"
                    contexts.append(text)
                else:
                    logger.warning(f"Unexpected document format: {type(doc)}")
                    continue

            if contexts:
                combined_context = "\n\n---\n\n".join(contexts)
                logger.info(f"Retrieved context with {len(contexts)} documents, total length: {len(combined_context)}")
                return combined_context
            else:
                logger.warning("No valid context found in documents")
                return None
        except Exception as e:
            logger.error(f"Error in retrieve_relevant_context: {str(e)}")
            raise
