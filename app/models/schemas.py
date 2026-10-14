from pydantic import BaseModel

class SummarizeRequest(BaseModel):
    test:str
    max_length:int=100

class AddDocsRequest(BaseModel):
    documents:list[str]

class RetrieveRequest(BaseModel):
    query:str
    n_results:int=5

    