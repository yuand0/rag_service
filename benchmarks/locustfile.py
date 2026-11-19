from locust import HttpUser, task, between
import random

class RAGUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def on_start(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-token-123"
        }

    @task(1)
    def health_check(self):
        self.client.get("/health")

    @task(3)
    def retrieve(self):
        queries = ["什么是机器学习？", "深度学习是什么？", "监督学习"]
        query = random.choice(queries)
        self.client.post("/retrieve", json={"query": query, "n_results": 2}, headers=self.headers)

    @task(2)
    def ask(self):
        queries = ["什么是机器学习？", "深度学习是什么？"]
        query = random.choice(queries)
        self.client.post("/ask", json={"query": query}, headers=self.headers)
