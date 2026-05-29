from fastapi import FastAPI
from velo_weather.backend.weather import get_weather
from velo_weather.backend.llm import get_clothing_recommendation

app = FastAPI()


@app.get("/api/weather/{city}")
def weather_endpoint(city: str) -> dict:
    return get_weather(city)


@app.get("/api/recommendation/{city}")
def recommendation_endpoint(city: str) -> dict:
    weather_data = get_weather(city)
    recommendation = get_clothing_recommendation(weather_data)
    return {"recommendation": recommendation}
