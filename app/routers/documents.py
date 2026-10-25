from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File
from pydantic import BaseModel
from app.services.vector_store import vector_store
from app.services.document_loader import loader_service
import os
import shutil

router=APIRouter()

UPLOAD_DIR="data/uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

async def verify_token(authorization:str=Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="缺少Authorization 头")
    token=authorization.replace("Bearer ","")
    if token !="test-token-123":
        raise HTTPException(status_code=403,detail="无效 token")
    return token

class AddDocsRequest(BaseModel):
    documents: list[str]

@router.post("/documents")
async def add_documents(req:AddDocsRequest,token:str=Depends(verify_token)):
    count=vector_store.add_documents(req.documents)
    return {"code":0,"data":{"added":count,"total":vector_store.count()},"message":"ok"}

@router.post("/documents/upload")
async def upload_file(file:UploadFile=File(...),token:str=Depends(verify_token)):
    file_path=os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path,"wb") as f:
        shutil.copyfileobj(file.file,f)

    try:
        chunks=loader_service.load_file(file_path)
        added=vector_store.add_langchain_documents(chunks)
        return{
            "code":0,
            "data":{
                "filename":file.filename,"chunks":len(chunks),"added":added,"total":vector_store.count()
            },
            "message":"ok"
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"文档处理失败:{e}")
    
@router.get("/documents/count")
async def get_count(token: str=Depends(verify_token)):
    return {"code":0,"data":{"total":vector_store.count()},"message":"ok"}


