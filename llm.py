import os
from groq import Groq
from typing import Optional, List, Any
from functools import partial

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

SYSTEM_RAG = (
    "You are a helpful assistant that answers strictly based on the provided context. "
    "If the answer is not in the context, say you don't know."
)

SYSTEM_WEATHER = (
    "You are a helpful weather assistant. Use the provided weather JSON to produce a clear, concise answer."
)

SYSTEM_SYNTH = (
    "You refine assistant responses for clarity, brevity (max ~6 sentences), and actionable phrasing."
)
def call_groq(prompt: str, temperature: float = 0.2) -> str:
    api = os.getenv("GROQ_API_KEY")

    if not api:

        q = prompt.lower()

        if any(w in q for w in ["weather", "temperature", "forecast", "rain", "humidity"]):
            return '{"mode":"weather","city":"mumbai"}'

        return '{"mode":"rag","city":null}'

    client = Groq(api_key=api)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return completion.choices[0].message.content



def get_chat_model(model: str = "llama-3.3-70b-versatile", temperature: float = 0.2):
    class _Wrapper:
        def __init__(self, temp):
            self.temperature = temp
        def invoke(self, prompt):
            return call_groq(prompt, temperature=self.temperature)

    return _Wrapper(temperature)


def get_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)

def rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", 
         "You are an accurate assistant. Answer ONLY using the information given in context. "
         "If the context is insufficient, say 'The context does not contain this information.'"),
        ("human", 
         "Question:\n{question}\n\n"
         "Context:\n{context}\n\n"
         "Answer ONLY based on the above context.")
    ])

def weather_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_WEATHER),
        ("human", "User question: {question}\n\nWeather data (JSON):\n{weather_json}\n\nWrite a 2-4 sentence answer.")
    ])

def router_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "Classify the user's question. Return ONLY valid JSON with keys: mode ('weather'|'rag'), city (string or null)."),
        ("human", "Question: {question}\nReturn JSON: {{\"mode\":..., \"city\":...}}")
    ])


def synth_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_SYNTH),
        ("human", "Original answer:\n{answer}\n\n Rewrite: keep facts, improve clarity, 1 short paragraph + bullets if appropriate.")
    ])
