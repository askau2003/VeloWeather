import requests
from fastapi import HTTPException
import numpy as np


def get_coordinates(city: str) -> tuple[float, float, str]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises HTTPError, if one occurred.
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
            "precipitation_probability,"
            "precipitation,"
            "wind_speed_10m,"
            "wind_gusts_10m,"
            "wind_direction_10m,"
            "uv_index,"
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
                "feels_like_c": feels_like(
                    hourly["temperature_2m"][i],
                    hourly["wind_speed_10m"][i],
                ),
                "precipitation_mm": hourly["precipitation"][i],
                "precipitation_probability_pct": hourly["precipitation_probability"][i],
                "windspeed_kmh": hourly["wind_speed_10m"][i],
                "wind_gusts_kmh": hourly["wind_gusts_10m"][i],
                "wind_direction_deg": hourly["wind_direction_10m"][i],
                "uv_index": hourly["uv_index"][i],
            }
            for i in range(len(times))
        ],
    }


def feels_like(temp_c, wind_kmh):
    temp_c = np.asarray(temp_c)
    wind_kmh = np.asarray(wind_kmh)

    wind_pow = np.power(wind_kmh, 0.16)

    return 13.12 + 0.6215 * temp_c - 11.37 * wind_pow + 0.3965 * temp_c * wind_pow
