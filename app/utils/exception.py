from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def global_exception_handler(request:Request,exc:Exception ):
    return JSONResponse(
        status_code=500,
        content={"code":500,"data":None,"message":f"服务器内部错误:{str(exc)}"}
    )

async def http_exception_handler(request:Request,exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code":exc.status_code,"data":None,"message":exc.detail}
    )

async def validation_exception_handler(request:Request,exc:RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"code":422,"data":None,"message":f"请求参数错误:{exc.errors()}"}
    )