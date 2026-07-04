"""
RAG Pipeline Module

This module sets up the components required for a Retrieval-Augmented Generation (RAG) pipeline,
including document loading, text splitting, embedding generation, and vector store management.
"""

from rag.loaders import LoaderInterface
from rag.splitters import SplitterInterface
from rag.vectorstores import VectorStoreInterface
import logging

class RAGIngestionPipeline:
    """
    A class to handle the ingestion of documents through the RAG pipeline.

    It uses a Loader to load documents, a Splitter to split them into chunks,
    and a VectorStore to store the chunks with their embeddings.

    Follow the Interfaces to implement custom components if needed.
    """
    def __init__(self, loader : LoaderInterface, splitter: SplitterInterface, vector_store: VectorStoreInterface):
        self.loader = loader
        self.splitter = splitter
        self.vector_store = vector_store.get_vector_store()

    def ingest(self, *filepaths):
        logging.info("Loading files :", *filepaths)
        docs= self.loader.load(*filepaths)
        logging.info("Splitting documents (", len(docs), ").")
        all_splits = self.splitter.split(docs)
        logging.info("Adding documents in the vector database.")
        return self.vector_store.add_documents(documents=all_splits)

class RAGQueryPipeline:
    """
    A class to handle the retrieval of information through the RAG pipeline.
    """
    def __init__(self, vector_store: VectorStoreInterface):
        self.vector_store = vector_store.get_vector_store()

    def query(self, query: str, k :int = 4):
        return self.vector_store.similarity_search(query, k=k)
