from llm import get_chat_model, synth_prompt

def synthesize(answer: str) -> str:
    llm = get_chat_model()
    prompt = synth_prompt().format(answer=answer)
    return llm.invoke(prompt)
