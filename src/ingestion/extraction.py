from docling.document_converter import DocumentConverter
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    @abstractmethod
    def extract_text(self, pdf_path: str) -> str:
        pass


class DoclingExtractor(BaseExtractor):
    def __init__(self):
        self.converter = DocumentConverter()
    def extract_text(self, pdf_path: str) -> str:
        result = self.converter.convert(pdf_path)
        markdown = result.document.export_to_markdown()
        return markdown
