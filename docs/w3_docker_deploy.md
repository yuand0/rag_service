# 加速W3: Docker 部署记录（2026.11.18）

## 镜像构建
- 基础镜像：python:3.12-slim
- CPU 版 torch（约 200MB）
- 清华源加速 pip 安装

## 运行命令

docker run -d \
  --name rag_service \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -v ~/.cache/chroma:/root/.cache/chroma \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -e OPENAI_API_KEY="sk-..." \
  -e OPENAI_BASE_URL="https://api.deepseek.com/v1" \
  -e HF_HUB_OFFLINE="1" \
  -e TRANSFORMERS_OFFLINE="1" \
  rag_service:v0.5.0

## 关键问题
1. 模型下载卡住 → 挂载宿主机 HF 缓存 + HF_HUB_OFFLINE=1
2. Chroma 模型下载慢 → 挂载 ~/.cache/chroma
3. chroma_db 锁冲突 → 先停宿主机 uvicorn

## 验证结果
- /health 返回 200
- /ask 返回答案 + 来源
