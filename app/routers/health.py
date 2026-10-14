from fastapi import APIRouter

router=APIRouter()

@router.get("/health")
def health():
    return {"code":0,"data":"ok","message":""}

