import os
from typing_extensions import override
from langchain_core.embeddings.embeddings import Embeddings
from langchain_community.embeddings import DashScopeEmbeddings


class MyEmbedding(Embeddings):
    """基于 DashScope 的嵌入模型，实现 LangChain Embeddings 接口"""

    def __init__(self, api_key: str = None):
        super().__init__()
        key = api_key or os.environ.get("DASHSCOPE_API_KEY", "")
        self._embedding = DashScopeEmbeddings(
            model="text-embedding-v4",
            dashscope_api_key=key,
        )

    @override
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embedding.embed_documents(texts)

    @override
    def embed_query(self, text: str) -> list[float]:
        return self._embedding.embed_query(text)
