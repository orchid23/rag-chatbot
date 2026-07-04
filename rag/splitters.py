from typing_extensions import override
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Iterable
from abc import ABC, abstractmethod

class SplitterInterface(ABC):
    """
    An interface for document splitters.
    
    Should implement a `split` method that takes a list of documents
    and returns a list of smaller, chunked documents.
    """
    @abstractmethod
    def split(self, documents : Iterable[Document]) -> List[Document]:
        pass

class DocumentSplitter(SplitterInterface):
    """A class to split documents into smaller chunks using RecursiveCharacterTextSplitter."""
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=True
        )
        
    @override
    def split(self, documents : Iterable[Document]) -> List[Document]:
        """
        Split a list of LangChain Documents into smaller chunks.

        Returns:
            List[Document]: smaller, chunked documents.
        """
        return self.splitter.split_documents(documents)