from fastapi import FastAPI
from velo_weather.backend.weather import get_weather

app = FastAPI()

@app.get("/api/weather/{city}")
def weather_endpoint(city: str) -> dict:
    return get_weather(city)