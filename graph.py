from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END
from langchain_core.documents import Document

from nodes.router import route_llm
from nodes.weather import fetch_weather, answer_weather
from nodes.rag import answer_from_context
from nodes.synthesis import synthesize

class AppState(TypedDict, total=False):
    question: str
    mode: str                  
    city: Optional[str]
    weather_json: dict
    context_docs: List[Document]
    answer: str
    retriever: any     


def build_graph(rag_retriever, weather_api_key: str):
    graph = StateGraph(AppState)

    def node_route(state: AppState) -> AppState:
        decision = route_llm(state["question"])
        out: AppState = {"mode": decision.get("mode", "rag")}
        if out["mode"] == "weather":
            out["city"] = decision.get("city") or "London"
        return out

    def node_weather(state: AppState) -> AppState:
        city = state.get("city") or "London"
        wjson = fetch_weather(city, api_key=weather_api_key)
        ans = answer_weather(state["question"], city, wjson)
        return {"weather_json": wjson, "answer": ans}

    def node_rag(state):
        q = state["question"].lower()

        # small friendly greetings handler
        if q in ["hi", "hello", "hey", "hii", "hai", "hiii"]:
            return {"answer": "Hi 👋! Upload a PDF and ask me anything about it OR ask me weather questions!"}

        docs = state["retriever"].invoke(state["question"])
        ans = answer_from_context(state["question"], docs)
        return {"answer": ans}

    def node_synth(state: AppState) -> AppState:
        final = synthesize(state["answer"])
        return {"answer": final}

    graph.add_node("route", node_route)
    graph.add_node("weather", node_weather)
    graph.add_node("rag", node_rag)
    graph.add_node("synth", node_synth)

    graph.add_edge(START, "route")

    def choose_branch(state: AppState):
        return state.get("mode", "rag")

    graph.add_conditional_edges(
        "route",
        choose_branch,
        {
            "weather": "weather",
            "rag": "rag",
        },
    )

    graph.add_edge("weather", "synth")
    graph.add_edge("rag", "synth")
    graph.add_edge("synth", END)

    return graph.compile()
