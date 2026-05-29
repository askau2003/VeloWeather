import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def get_clothing_recommendation(weather_data: dict) -> str:
    hourly = weather_data["hourly"]

    # Tag de næste 6 timer som udgangspunkt for anbefalingen
    next_hours = hourly[:6]

    avg_temp = sum(h["temperature_c"] for h in next_hours) / len(next_hours)
    avg_feels = sum(h["feels_like_c"] for h in next_hours) / len(next_hours)
    avg_wind = sum(h["windspeed_kmh"] for h in next_hours) / len(next_hours)
    max_precip = max(h["precipitation_probability_pct"] for h in next_hours)
    max_uv = max(h["uv_index"] for h in next_hours)

    prompt = f"""
Du er ekspert i påklædning til racercykling udendørs.
Baseret på følgende vejrforhold for de næste 6 timer, giv en konkret og praktisk påklædningsanbefaling til en racercyklist.

Vejrdata:
- By: {weather_data["city"]}
- Gennemsnitstemperatur: {avg_temp:.1f}°C
- Føles som: {avg_feels:.1f}°C
- Gennemsnitlig vindhastighed: {avg_wind:.1f} km/t
- Maks. nedbørssandsynlighed: {max_precip}%
- Maks. UV-indeks: {max_uv}

Angiv præcist hvilke lag og beklædningsgenstande der anbefales (f.eks. base layer, bib shorts, overtøj, handsker, hjelmhue osv.).
Vær kort og konkret — brug bullet points. Svar på dansk.
""".strip()

    response = _client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )
    return response.text
