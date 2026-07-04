import os
from typing_extensions import override
from langchain_core.embeddings.embeddings import Embeddings
from langchain_chroma import Chroma
from abc import ABC, abstractmethod


class VectorStoreInterface(ABC):
    """向量存储接口"""

    @abstractmethod
    def get_vector_store(self):
        pass

    @abstractmethod
    def add_documents(self, documents, ids=None):
        pass


class ChromaVectorStore(VectorStoreInterface):
    """基于 Chroma 的向量存储实现"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChromaVectorStore, cls).__new__(cls)
        return cls._instance

    def __init__(self, embedding: Embeddings, persist_dir: str, collection_name: str):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self._persist_dir = persist_dir
        self._collection_name = collection_name
        self.vector_store = Chroma(
            embedding_function=embedding,
            collection_name=collection_name,
            persist_directory=persist_dir,
        )

    @override
    def get_vector_store(self):
        return self.vector_store

    @override
    def add_documents(self, documents, ids=None):
        return self.vector_store.add_documents(documents, ids=ids)
