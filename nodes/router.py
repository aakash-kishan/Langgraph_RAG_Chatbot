import json
from typing import TypedDict, Optional

class RouteDecision(TypedDict, total=False):
    mode: str           
    city: Optional[str]

def route_llm(question: str) -> RouteDecision:
    q = question.lower()

    weather_words =  [
 "weather", "temperature", "rain", "forecast", "climate",
 "hot", "cold", "humid", "humidity", "heat", "sunny"
]

    if any(w in q for w in weather_words):
        words = q.replace("?", "").split()
        city = None
        for i, w in enumerate(words):
            if w in ["in", "at"]:
                if i+1 < len(words):
                    city = words[i+1].strip(",.")
                break

        return {"mode": "weather", "city": city if city else None}

    return {"mode": "rag", "city": None}
