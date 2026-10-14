from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.schemas import SummarizeRequest

router=APIRouter()
 
async def verify_token(authorization:str=Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,detail="缺少Authorization头")
    token=authorization.replace("Bearer ","")
    if token!="test-token-123":
        raise HTTPException(status_code=403,detail="无效Toekn")
    return token

@router.post("/summarize")
async def summarize(req:SummarizeRequest,token:str=Depends(verify_token)):
    if not req.text:
        raise HTTPException(status_code=400,detail="文本不能为空")
    return {"code":0,"data":{"summary":req.text[:req.max_length]},"message":"ok"}

