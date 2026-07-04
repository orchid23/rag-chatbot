from abc import ABC, abstractmethod
from typing_extensions import override
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from typing import List
from langchain_core.documents import Document


class LoaderInterface(ABC):
    """文档加载器接口"""

    @abstractmethod
    def load(self, *filepaths: str) -> List[Document]:
        pass


class PDFLoader(LoaderInterface):
    """PDF 文档加载器"""

    @override
    def load(self, *filepaths: str) -> List[Document]:
        documents = []
        for path in filepaths:
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
        return documents


class TXTLoader(LoaderInterface):
    """TXT 文档加载器"""

    @override
    def load(self, *filepaths: str) -> List[Document]:
        documents = []
        for path in filepaths:
            loader = TextLoader(path, encoding='utf-8')
            documents.extend(loader.load())
        return documents


class AutoLoader(LoaderInterface):
    """自动根据文件后缀选择加载器"""

    @override
    def load(self, *filepaths: str) -> List[Document]:
        documents = []
        for path in filepaths:
            if path.endswith('.pdf'):
                loader = PyPDFLoader(path)
            elif path.endswith('.txt'):
                loader = TextLoader(path, encoding='utf-8')
            else:
                print(f"⚠️ 不支持的文件格式: {path}，跳过")
                continue
            documents.extend(loader.load())
        return documents
