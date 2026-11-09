from sentence_transformers import CrossEncoder


class Reranker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("[Reranker] 加载 BGE-reranker-base 模型...")
            cls._instance._model = CrossEncoder(
                "BAAI/bge-reranker-base",
                max_length=512
            )
            print("[Reranker] 模型加载完成")
        return cls._instance

    def rerank(self, query: str, documents: list[str], top_k: int = 3) -> list:
        """对文档重排序，返回 Top-K"""
        if not documents:
            return []
        pairs = [[query, doc] for doc in documents]
        scores = self._model.predict(pairs)
        ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        print(f"[Reranker] 重排序 {len(documents)} 个文档 → Top-{top_k}")
        return [doc for doc, _ in ranked[:top_k]]


reranker = Reranker()
