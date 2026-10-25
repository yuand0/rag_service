from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.routers import health, summarize, retrieve, documents
from app.utils.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)

app = FastAPI(
    title="RAG Knowledge Base API",
    version="0.3.0",
    description="基于 FastAPI + Chroma + C++ 组件的 RAG 知识库问答系统"
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(health.router, tags=["Health"])
app.include_router(summarize.router, tags=["Summarize"])
app.include_router(retrieve.router, tags=["Retrieve"])
app.include_router(documents.router, tags=["Documents"])
