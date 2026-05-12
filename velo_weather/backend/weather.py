import requests
from fastapi import HTTPException

def get_coordinates(city: str) -> tuple[float, float, str]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise HTTPException(status_code=404, detail=f"Kunne ikke finde by: '{city}'")

    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"]

def get_weather(city: str) -> dict:
    lat, lon, resolved_name = get_coordinates(city)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": (
            "temperature_2m,"
            "apparent_temperature,"
            "precipitation_probability,"
            "precipitation,"
            "wind_speed_10m,"
            "wind_gusts_10m,"
            "wind_direction_10m,"
            "uv_index,"
            "cloud_cover"
        ),
        "forecast_days": 1,
        "timezone": "auto",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    hourly = response.json()["hourly"]

    times = hourly["time"]
    return {
        "city": resolved_name,
        "hourly": [
            {
                "time": times[i],
                "temperature_c": hourly["temperature_2m"][i],
                "feels_like_c": hourly["apparent_temperature"][i],
                "precipitation_mm": hourly["precipitation"][i],
                "precipitation_probability_pct": hourly["precipitation_probability"][i],
                "windspeed_kmh": hourly["wind_speed_10m"][i],
                "wind_gusts_kmh": hourly["wind_gusts_10m"][i],
                "wind_direction_deg": hourly["wind_direction_10m"][i],
                "uv_index": hourly["uv_index"][i],
                "cloud_cover_pct": hourly["cloud_cover"][i],
            }
            for i in range(len(times))
        ],
    }