import os
from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA


def get_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.environ.get("OPENAI_API_KEY",""),
        base_url=os.environ.get("OPENAI_BASE_URL","https://api.deepseek.com/v1"),
        temperature=0.3
    )

def build_rag_chain(vector_store):
    retriever=vector_store.as_retriever()
    chain=RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain
