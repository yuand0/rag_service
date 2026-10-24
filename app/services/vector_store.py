import chromadb
from chromadb.config import Settings
import hashlib
import os
from app.services.cpp_bridge import cpp_bridge

# 持久化目录
CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")


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

    def similarity_search(self, query: str, n_results: int = 5):
        tokens = cpp_bridge.tokenize(query, self.dict_words)
        if all(len(t) <= 1 for t in tokens):
            processed_query = query
            print(f"[C++] 分词效果差，回退原始查询: {query}")
        else:
            processed_query = ' '.join(tokens)
            print(f"[C++] 原始查询: {query} → 分词后: {processed_query}")

        results = self.collection.query(
            query_texts=[processed_query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

    def count(self):
        return self.collection.count()


vector_store = VectorStore()
