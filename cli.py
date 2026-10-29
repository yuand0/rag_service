#!/usr/bin/env python3
import os
import sys

sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

from app.services.vector_store import vector_store
from app.services.rag_chain import build_rag_chain

def main():
    print("="*50)
    print("RAG知识库问答(输入 'exit' 退出)")
    print("="*50)

    chain=build_rag_chain(vector_store)

    while True:
        try:
            query=input("\n ? 问题: ").strip()
        except(EOFError,KeyboardInterrupt):
            print("\n再见!")
            break

        if query.lower() in ("exit","quit","q"):
            print("再见!")
            break
        if not query:
            continue

        print("搜索中...")
        try:
            result=chain.invoke({"query":query})
            print(f"\n 答案:{result['result']}")
            print(f"\n 来源:({len(result['source_documents'])}个):")
            for i,doc in enumerate(result["source_documents"],1):
                snippet =doc.page_content[:80].replace("\n"," ")
                print(f" {i}.{snippet}...")
        except Exception as e:
            print(f" 出错: {e}")

if __name__=="__main__":
    main()


    






