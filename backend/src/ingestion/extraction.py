from docling.document_converter import DocumentConverter
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
        Abstract Base Class (ABC) defining the required interface for a text extraction service.

        Any concrete class used for extracting readable text (e.g., Markdown) from
        documents (e.g., PDFs) must inherit from this class and implement the
        abstract methods.
    """
    @abstractmethod
    async def extract_text(self, pdf_path: str) -> str:
        """
            Asynchronously extracts text content from a specified document file path.
            Args:
                pdf_path (str): The file path to the document (e.g., a PDF) to be processed.
            Returns:
                str: The extracted text content, typically formatted as Markdown.
        """
        pass


class DoclingExtractor(BaseExtractor):
    """
        Concrete implementation of BaseExtractor that uses the Docling library
        (via DocumentConverter) to convert documents, such as PDFs, into Markdown text.
    """
    def __init__(self):
        """
            Initializes the Docling DocumentConverter instance, which is used for
            handling the document conversion logic.
        """
        self.converter = DocumentConverter()
    async def extract_text(self, pdf_path: str) -> str:
        """
            Asynchronously extracts text from a PDF file using the Docling DocumentConverter.
            The process involves:
            1. Converting the document using `self.converter.convert(pdf_path)`.
            2. Exporting the result's document object to a Markdown string.
            Args:
                pdf_path (str): The file path to the PDF document.
            Returns:
                str: The extracted content formatted as a Markdown string.
        """
        result = self.converter.convert(pdf_path)
        markdown = result.document.export_to_markdown()
        return markdown
