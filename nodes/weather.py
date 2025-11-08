from typing import Dict, Any
import requests
import json
from llm import get_chat_model, weather_prompt

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str, api_key: str, units: str = "metric") -> Dict[str, Any]:
    params = {"q": city, "appid": api_key, "units": units}
    r = requests.get(OPENWEATHER_URL, params=params, timeout=15)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return {"error":"no weather"}

def answer_weather(question: str, city: str, weather_json: Dict[str, Any]) -> str:
    llm = get_chat_model()
    prompt = weather_prompt().format(question=question, weather_json=json.dumps(weather_json, ensure_ascii=False))
    return llm.invoke(prompt)
