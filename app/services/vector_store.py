import chromadb
from chromadb.config import Settings
import hashlib

class VectorStore:
    def __init__(self, collection_name: str = "knowledge_base"):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(collection_name)
    
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
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []
    
    def count(self):
        return self.collection.count()

vector_store = VectorStore()
