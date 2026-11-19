import chromadb
from chromadb.config import Settings
import hashlib
import os
from app.services.cpp_bridge import cpp_bridge
from app.services.reranker import reranker
from app.services.hyde import generate_hypothetical_answer
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List
from pydantic import Field

CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")


class CppRetriever(BaseRetriever):
    store: object = Field(...)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        results = self.store.similarity_search(query, n_results=3)
        return [Document(page_content=r) for r in results]


class VectorStore:
    def __init__(self, collection_name: str = "knowledge_base"):
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.dict_words = {
            '人工智能', '机器学习', '深度学习', '神经网络', '计算机',
            '科学', '技术', '模型', '数据', '算法', '自然语言',
            '处理', '监督', '学习', '无监督', '强化', '回归',
            '分类', '聚类', '降维', '决策', '支持向量机', '什么',
            '是', '的', '和', '与', '在', '应用', '领域', '研究'
        }

    def add_documents(self, documents: list[str], metadatas: list[dict] = None):
        ids = [hashlib.sha256(doc.encode()).hexdigest()[:16] for doc in documents]
        if metadatas:
            self.collection.add(documents=documents, ids=ids, metadatas=metadatas)
        else:
            self.collection.add(documents=documents, ids=ids)
        return len(documents)

    def add_langchain_documents(self, chunks):
        documents = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        metadatas = [m if m else {"source": "unknown"} for m in metadatas]
        return self.add_documents(documents, metadatas)

    def similarity_search(self, query: str, n_results: int = 5, use_hyde: bool = False):
        original_query = query

        if use_hyde:
            try:
                hypo = generate_hypothetical_answer(query)
                print(f"[HyDE] 原问题: {query}")
                print(f"[HyDE] 假设答案: {hypo[:100]}...")
                query = hypo
            except Exception as e:
                print(f"[HyDE] 生成失败，回退原始查询: {e}")

        tokens = cpp_bridge.tokenize(query, self.dict_words)
        if all(len(t) <= 1 for t in tokens):
            processed_query = query
            print(f"[C++] 分词效果差，回退原始查询: {query}")
        else:
            processed_query = ' '.join(tokens)
            print(f"[C++] 原始查询: {query} → 分词后: {processed_query}")

        recall_n = max(n_results * 2, 5)
        results = self.collection.query(
            query_texts=[processed_query],
            n_results=recall_n
        )
        docs = results['documents'][0] if results['documents'] else []

        if docs:
            return reranker.rerank(original_query, docs, top_k=n_results)
        return []

    def count(self):
        return self.collection.count()

    def as_retriever(self, **kwargs):
        return CppRetriever(store=self)


vector_store = VectorStore()
