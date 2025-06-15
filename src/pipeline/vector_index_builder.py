import os
import json
import numpy as np
from typing import List, Dict, Any, Optional

from config.settings import settings
from src.knowledge_base.pdf_loader import PDFLoader
from src.knowledge_base.text_processor import TextProcessor
from src.knowledge_base.vector_store import VectorStore
from src.utils.logger import logger


class VectorIndexBuilder:
    def __init__(self, pdf_dir: Optional[str] = None):
        """
        初始化向量索引构建器
        
        Args:
            pdf_dir: PDF文件目录，如果为None则使用settings中的默认目录
        """
        self.pdf_dir = pdf_dir or settings.RAW_PAPERS_DIR
        self.pdf_loader = PDFLoader(self.pdf_dir)
        self.text_processor = TextProcessor()
        self.vector_store = VectorStore()

    def process_documents(self) -> List[Dict]:
        """处理所有文档并返回处理后的文本块"""
        all_processed_chunks = []
        pdf_files = self.pdf_loader.load_pdfs()
        logger.info(f"共检测到PDF文件：{len(pdf_files)}")
        
        for pdf_path in pdf_files:
            results = self.pdf_loader.load_pdf(pdf_path)
            if not results:
                logger.warning(f"未能读取：{pdf_path}")
                continue
                
            for doc in results:
                chunks = self.text_processor.process_document(doc)
                all_processed_chunks.extend(chunks)
                
        logger.info(f"生成了 {len(all_processed_chunks)} 个文本块")
        return all_processed_chunks

    def save_processed_chunks(self, chunks: List[Dict]) -> str:
        """保存处理后的文本块到JSON文件"""
        os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
        processed_file = os.path.join(settings.PROCESSED_DIR, "processed_chunks.json")
        
        with open(processed_file, "w", encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
            
        logger.info(f"已保存处理后的文本块到：{processed_file}")
        return processed_file

    def build_index(self, chunks: Optional[List[Dict]] = None) -> None:
        """
        构建或重建向量索引
        
        Args:
            chunks: 可选的文本块列表，如果为None则重新处理所有文档
        """
        if chunks is None:
            chunks = self.process_documents()
            
        all_docs = []
        all_vecs = []
        
        for chunk in chunks:
            all_docs.append({
                'text': chunk['text'],
                'source': chunk['metadata'].get('source', ''),
                'chunk_index': chunk['metadata'].get('chunk_index', 0)
            })
            all_vecs.append(self.vector_store.model.encode(chunk['text']))

        all_vecs = np.array(all_vecs)
        save_data = {'documents': all_docs, 'vectors': all_vecs.tolist()}
        
        # 确保输出目录存在
        os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
        
        out_path = os.path.join(settings.VECTOR_DB_DIR, 'vector_index.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f'向量索引重建完成，文献分块数：{len(all_docs)}，输出文件：{out_path}')

    def run_pipeline(self) -> None:
        """运行完整的数据处理管道"""
        try:
            # 1. 处理文档
            chunks = self.process_documents()
            
            # 2. 保存处理后的文本块
            self.save_processed_chunks(chunks)
            
            # 3. 构建向量索引
            self.build_index(chunks)
            
            logger.info("数据处理管道完成")
            
        except Exception as e:
            logger.error(f"数据处理管道执行失败: {str(e)}")
            raise


def main():
    """命令行入口函数"""
    try:
        builder = VectorIndexBuilder()
        builder.run_pipeline()
    except Exception as e:
        logger.error(f"重建向量索引时发生错误: {str(e)}")
        raise


if __name__ == "__main__":
    main() 