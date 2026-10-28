from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from app.services.vector_store import vector_store
from app.services.rag_chain import build_rag_chain

router=APIRouter()

_rag_chain=None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain=build_rag_chain(vector_store)
    return _rag_chain

async def verify_token(authorization:str=Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="缺少Authorization 头")
    token=authorization.replace("Bearer ","")
    if token !="test-token-123":
        raise HTTPException(status_code=403,detail="无效 Token")
    return token

class AskRequest(BaseModel):
    query:str

@router.post("/ask")
async def ask(req:AskRequest,token:str=Depends(verify_token)):
    if not req.query.strip():
        raise HTTPException(status_code=400,detail="问题不能为空")
    
    try:
        chain=get_rag_chain()
        result=chain.invoke({"query":req.query})
        return{
            "code":0,
            "data":{
                "query":req.query,
                "answer":result["result"],
                "sources":[doc.page_content[:200] for doc in result["source_documents"]]
            },
            "message":"ok"
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"RAG 问答失败 :{e}")


