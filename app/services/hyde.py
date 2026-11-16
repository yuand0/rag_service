from app.services.rag_chain import get_llm


def generate_hypothetical_answer(query: str) -> str:
    """HyDE: LLM 生成假设答案，用于检索"""
    llm = get_llm()
    prompt = f"""请针对以下问题，生成一段简洁的假设性答案。无需完全准确，只需覆盖可能的关键信息（如术语、概念、关系）。

问题：{query}

假设答案："""
    response = llm.invoke(prompt)
    return response.content.strip()
