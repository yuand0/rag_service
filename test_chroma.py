import chromadb

client = chromadb.Client()
collection = client.create_collection("test")

collection.add(
    documents=["你好世界", "人工智能", "机器学习"],
    ids=["1", "2", "3"]
)

results = collection.query(query_texts=["人工智能"], n_results=2)
print("查询结果:", results['documents'])
