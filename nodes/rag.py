import os
from llm import get_chat_model, rag_prompt

def answer_from_context(question: str, docs):
    llm = get_chat_model()
    context = "\n\n".join([d.page_content for d in docs])
    prompt = rag_prompt().format(question=question, context=context)
    return llm.invoke(prompt)
