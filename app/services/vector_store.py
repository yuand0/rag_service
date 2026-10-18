import chromadb
from chromadb.config import Settings
import hashlib
from app.services.cpp_bridge import cpp_bridge

class VectorStore:
    def __init__(self, collection_name: str = "knowledge_base"):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(collection_name)
        self.dict_words={
            '人工智能','机械学习','深度学习','神经网络','计算机',
            '网络','科学','技术','模型','数据','算法'
        }
    
    def add_documents(self, documents: list[str], metadatas: list[dict] = None):
        ids = [hashlib.sha256(doc.encode()).hexdigest()[:16] for doc in documents]
        
        if metadatas:
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
        else:
            # 不传 metadatas，避免空字典错误
            self.collection.add(
                documents=documents,
                ids=ids
            )
        return len(documents)
    
    def similarity_search(self, query: str, n_results: int = 5):
        tokens=cpp_bridge.tokenize(query,self.dict_words)
        processed_query=' '.join(tokens)
        print(f"[C++]原始查询:{query}->分词后:{processed_query}")

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []
    
    def count(self):
        return self.collection.count()

vector_store = VectorStore()
