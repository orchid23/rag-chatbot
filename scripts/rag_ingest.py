"""
向 Chroma 向量库导入文档（支持 PDF 和 TXT）
用法: python scripts/rag_ingest.py <文件路径1> <文件路径2> ...
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.loaders import AutoLoader
from rag.splitters import DocumentSplitter
from rag.vectorstores import ChromaVectorStore
from rag.embeddings import MyEmbedding
from rag.pipelines import RAGIngestionPipeline
from dotenv import load_dotenv
load_dotenv()

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = os.getenv("VECTOR_DB_COLLECTION", "rag_collection")

loader = AutoLoader()
splitter = DocumentSplitter(chunk_size=1000, chunk_overlap=200)
embedding = MyEmbedding()
vector_store = ChromaVectorStore(
    embedding=embedding,
    persist_dir=PERSIST_DIR,
    collection_name=COLLECTION_NAME,
)

ingestion_pipeline = RAGIngestionPipeline(loader, splitter, vector_store)

if len(sys.argv) < 2:
    # 默认导入 data/ 目录下所有文件
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    files = []
    if os.path.isdir(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith(('.pdf', '.txt')):
                files.append(os.path.join(data_dir, f))
    if not files:
        print("未找到可导入的文件。用法: python scripts/rag_ingest.py <文件> [...]")
        sys.exit(1)
    print(f"找到 {len(files)} 个文件待导入: {[os.path.basename(f) for f in files]}")
    files_to_ingest = files
else:
    files_to_ingest = sys.argv[1:]

ingestion_pipeline.ingest(*files_to_ingest)
print(f"文档导入完成! 共处理 {len(files_to_ingest)} 个文件")
