# RAG 知识库问答系统 — 架构设计

## 系统架构图

[用户]
  │
  ▼
[FastAPI 网关] ──(Depends 鉴权)── [JWT Token 校验]
  │
  ├── /health    ──> 探活
  ├── /documents ──> 文档上传 ──> [LangChain Loader] ──> [递归分割器] ──> [Chroma 向量库]
  ├── /retrieve  ──> [C++ 分词器] ──> [Chroma 检索 Top-10] ──> [BGE-reranker 重排 Top-3]
  └── /ask       ──> [HyDE] ──> (同上检索流程) ──> [DeepSeek LLM 生成]

[底层 C++ 组件] (cpp_core.so)
  ├── Tokenizer   (中文最大匹配分词)
  ├── Cosine      (余弦相似度加速计算)
  └── Calculator  (表达式求值)

## 核心数据流

1. 离线入库：PDF/TXT -> 文本分割 -> C++ 分词预处理 -> 向量化存入 Chroma。
2. 在线检索：用户提问 -> (HyDE 假设答案生成) -> C++ 分词 -> 向量召回 Top-10 -> BGE 重排 Top-3。
3. 生成回答：将重排后的上下文与问题拼接，调用 DeepSeek 生成最终答案。
