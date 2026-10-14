from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError 
from app.routers import health, summarize, retrieve
from app.utils.exception import global_exception_handler, http_exception_handler,validation_exception_handler

app=FastAPI(title="RAG knowledge Base API",version="0.1.0",description="基于FastAPI+Chroma+C++组件的RAG知识库问答系统")

app.add_exception_handler(Exception,global_exception_handler)
app.add_exception_handler(HTTPException,http_exception_handler)
app.add_exception_handler(RequestValidationError,validation_exception_handler)

app.include_router(health.router,tags=["Health"])
app.include_router(summarize.router,tags=["Summarize"])
app.include_router(retrieve.router,tags=["Retrieve"])

