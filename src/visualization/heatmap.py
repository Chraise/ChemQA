import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
from src.knowledge_base.retriever import Retriever

class HeatmapVisualizer:
    def __init__(self):
        """初始化热力图可视化器"""
        self.retriever = Retriever()
        
    def generate_organic_electrocatalysis_queries(self) -> List[str]:
        """
        生成5个与有机电催化相关的英文查询
        
        Returns:
            查询文本列表
        """
        queries = [
            "mechanism of CO2 electroreduction on Cu single-atom catalysts",
            "electrochemical oxidation of alcohols to aldehydes",
            "electrochemical C-H functionalization of arenes",
            "electrochemical synthesis of heterocyclic compounds",
            "electrochemical reduction of carbonyl compounds"
        ]
        return queries
        
    def create_similarity_heatmap(self, 
                                queries: List[str] = None,
                                max_docs: int = 15,  # 显示前15个最相关文档
                                figsize: tuple = (12, 8),
                                cmap: str = 'viridis',  # 改为viridis以提高区分度
                                vmin: float = 0.4,  # 调整最小值为0.4
                                vmax: float = 0.8,  # 调整最大值为0.8
                                save_path: str = None) -> None:
        """
        创建查询-文档相似度热力图
        
        Args:
            queries: 查询文本列表，如果为None则使用默认的有机电催化查询
            max_docs: 显示的最相关文档数量
            figsize: 图像大小
            cmap: 颜色映射
            vmin: 颜色映射最小值
            vmax: 颜色映射最大值
            save_path: 保存图像的路径，如果为None则显示图像
        """
        # 如果没有提供查询，使用默认的有机电催化查询
        if queries is None:
            queries = self.generate_organic_electrocatalysis_queries()
            
        print(f"Processing {len(queries)} queries...")
        
        # 获取所有文档
        all_docs = self.retriever.vector_store.vector_index.get("documents", [])
        if not all_docs:
            print("No documents found in vector store")
            return
            
        print(f"Found {len(all_docs)} total documents")
        
        # 创建相似度矩阵
        similarity_matrix = np.zeros((len(all_docs), len(queries)))
        
        # 对每个查询计算与所有文档的相似度
        for i, query in enumerate(queries):
            print(f"Processing query {i+1}/{len(queries)}: {query[:50]}...")
            
            # 将查询转换为向量
            query_vector = self.retriever.vector_store.model.encode(query)
            
            # 计算与所有文档的相似度
            for j, doc in enumerate(all_docs):
                # 获取文档文本
                doc_text = doc.get("text", "")
                if doc_text:
                    # 将文档转换为向量
                    doc_vector = self.retriever.vector_store.model.encode(doc_text)
                    
                    # 计算余弦相似度
                    similarity = np.dot(query_vector, doc_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(doc_vector))
                    similarity_matrix[j, i] = similarity
        
        # 选择最相关的文档
        # 计算每个文档的平均相似度（跨所有查询）
        avg_similarities = np.mean(similarity_matrix, axis=1)
        
        # 选择平均相似度最高的max_docs个文档
        top_doc_indices = np.argsort(avg_similarities)[-max_docs:][::-1]
        
        # 提取这些文档的相似度矩阵
        selected_similarity_matrix = similarity_matrix[top_doc_indices]
        
        # 创建文档标签（改为chunk）
        doc_labels = [f"Chunk{i+1}" for i in range(max_docs)]
        
        # 设置matplotlib字体大小
        plt.rcParams.update({'font.size': 18})  # 进一步增大默认字体大小
        
        # 创建热力图
        plt.figure(figsize=figsize)
        
        # 创建热力图，纵轴显示chunk编号
        sns.heatmap(selected_similarity_matrix,
                   xticklabels=[f"Q{i+1}" for i in range(len(queries))],
                   yticklabels=doc_labels,
                   cmap=cmap,
                   vmin=vmin,
                   vmax=vmax,
                   annot=True,
                   fmt='.2f',
                   annot_kws={'size': 16},  # 进一步增大注释文字大小
                   cbar_kws={'label': 'Cosine Similarity'})
        
        # 设置标题和标签（进一步增大字号）
        plt.title('Organic Electrocatalysis Query-Chunk Similarity Heatmap', fontsize=24, fontweight='bold')
        plt.xlabel('Queries', fontsize=20)
        plt.ylabel('Text Chunks', fontsize=20)
        
        # 进一步增大刻度标签字号
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        
        # 进一步增大颜色条标签字号
        cbar = plt.gcf().axes[-1]
        cbar.set_ylabel('Cosine Similarity', fontsize=20)
        cbar.tick_params(labelsize=18)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存或显示图像
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Heatmap saved to: {save_path}")
        else:
            plt.show()
            
        # 打印查询详情
        print("\nQuery Details:")
        for i, query in enumerate(queries):
            print(f"Q{i+1}: {query}")
            
        # 打印文档详情
        print("\nChunk Details:")
        for i, doc_idx in enumerate(top_doc_indices):
            doc = all_docs[doc_idx]
            metadata = doc.get("metadata", {})
            title = metadata.get("title", "")
            if title:
                print(f"Chunk{i+1}: {title}")
            else:
                text = doc.get("text", "")[:50]
                print(f"Chunk{i+1}: {text}...") 