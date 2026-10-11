from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from app.services.vector_store import vector_store

app = FastAPI(title="RAG Knowledge Base API", version="0.1.0")

async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="缺少 Authorization 头")
    token = authorization.replace("Bearer ", "")
    if token != "test-token-123":
        raise HTTPException(status_code=403, detail="无效 Token")
    return token

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 100

class AddDocsRequest(BaseModel):
    documents: list[str]

class RetrieveRequest(BaseModel):
    query: str
    n_results: int = 5

@app.get("/health")
def health():
    return {"code": 0, "data": "ok", "message": ""}

@app.post("/summarize")
async def summarize(req: SummarizeRequest, token: str = Depends(verify_token)):
    if not req.text:
        raise HTTPException(status_code=400, detail="文本不能为空")
    return {"code": 0, "data": {"summary": req.text[:req.max_length]}, "message": "ok"}

@app.post("/documents")
async def add_documents(req: AddDocsRequest, token: str = Depends(verify_token)):
    count = vector_store.add_documents(req.documents)
    return {"code": 0, "data": {"added": count, "total": vector_store.count()}, "message": "ok"}

@app.post("/retrieve")
async def retrieve(req: RetrieveRequest, token: str = Depends(verify_token)):
    results = vector_store.similarity_search(req.query, req.n_results)
    return {"code": 0, "data": {"query": req.query, "results": results}, "message": "ok"}
