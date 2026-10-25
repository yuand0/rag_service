from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.schemas import AddDocsRequest, RetrieveRequest
from app.services.vector_store import vector_store

router=APIRouter()

async def verify_token(authorization:str=Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="缺少Authorization头")
    token=authorization.replace("Bearer ","")
    if token!="test-token-123":
        raise HTTPException(status_code=403,detail="无效token")
    return token        


@router.post("/retrieve")
async def retrieve(req:RetrieveRequest,token:str=Depends(verify_token)):
    results=vector_store.similarity_search(req.query,req.n_results)
    return{"code":0,"data":{"query":req.query,"results":results},"message":"ok"}