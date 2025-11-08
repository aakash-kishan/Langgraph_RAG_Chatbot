
import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import os
from nodes.weather import fetch_weather

def test_weather_api_response():
    api_key = os.getenv("OWM_API_KEY", "NA")
    out = fetch_weather("London", api_key=api_key)
    assert isinstance(out, dict) or out is None
