import os
from typing import List, Dict, Optional

import fitz  # PyMuPDF

from config.settings import settings
from src.utils.logger import logger


class PDFLoader:
    def __init__(self, pdf_dir: Optional[str] = None):
        self.pdf_dir = pdf_dir or settings.RAW_PAPERS_DIR

    def load_pdfs(self) -> List[str]:
        """获取所有PDF文件路径"""
        pdf_files = []
        for root, dirs, files in os.walk(self.pdf_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files

    def load_pdf(self, pdf_path: str) -> List[Dict]:
        """加载单个PDF文件并返回其内容"""
        try:
            if not os.path.exists(pdf_path):
                logger.error(f"PDF file not found: {pdf_path}")
                return []

            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()

            if not text.strip():
                logger.warning(f"No text content found in {pdf_path}")
                return []

            metadata = {
                "source": pdf_path,
                "title": os.path.basename(pdf_path),
                "total_pages": len(doc),
            }

            return [{"text": text, "metadata": metadata}]

        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            return []

    def extract_text(self, pdf_path: str) -> Dict[str, str]:
        """提取PDF文本内容和元数据"""
        results = self.load_pdf(pdf_path)
        return results[0] if results else {"text": "", "metadata": {}}

