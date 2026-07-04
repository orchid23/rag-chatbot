# Need to add the modules to the path for imports
import unittest, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from langchain_core.documents import Document
from rag.splitters import DocumentSplitter

class TestSplitters(unittest.TestCase):

    def setUp(self):
        self.long_text = " ".join([f"Sentence {i}." for i in range(50)])
        self.doc = Document(page_content=self.long_text, metadata={"source": "test.pdf"})
        self.chunk_size = 100
        self.chunk_overlap = 20
        self.splitter = DocumentSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def test_splitter_returns_list_of_documents(self):
        all_splits = self.splitter.split([self.doc])
        self.assertIsInstance(all_splits, list)
        self.assertTrue(all(isinstance(chunk, Document) for chunk in all_splits))

    def test_chunks_respect_size_and_overlap(self):
        all_splits = self.splitter.split([self.doc])
        for i, chunk in enumerate(all_splits):
            self.assertLessEqual(len(chunk.page_content), self.chunk_size)

if __name__ == "__main__":
    unittest.main()