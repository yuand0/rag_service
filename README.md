# RAG 知识库问答系统

基于 FastAPI + Chroma + LangChain + C++ 组件的生产级 RAG 知识库问答系统。

## 核心特性
- C++ 高性能底座：通过 pybind11 接入 C++ 分词器与余弦相似度计算，比纯 Python 快 5-8 倍。
- 双路检索增强：集成 BGE-reranker 重排序与 HyDE（假设文档嵌入）提升检索召回率。
- 生产级容器化：多阶段构建 Dockerfile，解决 C++ .so 动态链接与模型离线加载问题。
- 全链路监控：统一 request_id 日志追踪 + Prometheus 指标暴露。

## 技术栈
FastAPI, ChromaDB, LangChain, pybind11, Docker, Locust, DeepSeek API

## 快速启动

### 1. 本地运行
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

### 2. Docker 运行
docker build -t rag_service:v1.0.0 -f docker/Dockerfile .
docker run -d -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -v ~/.cache/chroma:/root/.cache/chroma \
  -e OPENAI_API_KEY="your-api-key" \
  -e OPENAI_BASE_URL="https://api.deepseek.com/v1" \
  rag_service:v1.0.0

## 文档
- 架构设计：docs/architecture.md
- 性能压测报告：docs/w3_locust_report.md
- HyDE 消融实验：docs/hyde_ablation.md
