import re
from typing import List, Dict

from config.settings import settings


class TextProcessor:
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def clean_text(self, text: str) -> str:
        """清理文本中的无用字符"""
        # 删除多余的空格和换行
        text = re.sub(r'\s+', ' ', text)
        # 删除特殊字符（保留常见标点）
        text = re.sub(r'[^\w\s,.?;:!-]', '', text)
        return text.strip()

    def split_text(self, text: str) -> List[str]:
        """将长文本分割为指定大小的块"""
        chunks = []
        words = text.split()

        start_idx = 0
        while start_idx < len(words):
            end_idx = min(start_idx + self.chunk_size, len(words))
            chunk = " ".join(words[start_idx:end_idx])
            chunks.append(chunk)

            # 设置重叠部分
            start_idx += self.chunk_size - self.chunk_overlap

        return chunks

    def add_metadata(self, chunk: str, metadata: Dict, chunk_idx: int) -> Dict:
        """为文本块添加元数据"""
        new_meta = metadata.copy()
        new_meta.update({
            "chunk_index": chunk_idx,
            "num_tokens": len(chunk.split())
        })
        return {"text": chunk, "metadata": new_meta}

    def process_document(self, document: Dict) -> List[Dict]:
        """处理单个文档"""
        cleaned_text = self.clean_text(document["text"])
        text_chunks = self.split_text(cleaned_text)

        processed_chunks = []
        for idx, chunk in enumerate(text_chunks):
            processed_chunks.append(
                self.add_metadata(chunk, document["metadata"], idx)
            )

        return processed_chunks
