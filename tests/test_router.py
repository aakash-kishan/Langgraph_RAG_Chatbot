from nodes.router import route_llm
import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_weather_routing():
    # question clearly about weather
    result = route_llm("how is the weather in mumbai?")
    assert result["mode"] == "weather"

def test_rag_routing():
    # question clearly about knowledge
    result = route_llm("what does the pdf say about vector databases?")
    assert result["mode"] == "rag"
