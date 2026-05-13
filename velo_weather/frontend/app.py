import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="VeloWeather", page_icon="🚴", layout="wide")
st.title("VeloWeather")

# Gem city som variabel, så den kan bruges som parameter på api kaldet
city = st.text_input("Søg efter by", placeholder="København")

if city:
    with st.spinner("Henter vejrdata..."):
        req = requests.get(f"{API_BASE}/api/weather/{city}")

    if req.status_code == 404:
        st.error(f"Kunne ikke finde by: '{city}'")
        st.stop()
    elif req.status_code != 200:
        st.error("Noget gik galt - prøv igen")
        st.stop()

    data = req.json()
    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])

    st.subheader(f"Vejr i {data['city']} - {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}") # lokal tid

    # --- Metrics ---
    now = df.iloc[pd.Timestamp.now().hour]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌡️ Temperatur", f"{now['temperature_c']} °C", f"Føles som {now['feels_like_c']} °C")
    col2.metric("💨 Vind", f"{now['windspeed_kmh']} km/t", f"Vindstød {now['wind_gusts_kmh']} km/t")
    col3.metric("🌧️ Nedbør", f"{now['precipitation_mm']} mm", f"{now['precipitation_probability_pct']}% sandsynlighed")
    col4.metric("☀️ UV-indeks", now["uv_index"])

    def fmt_xaxis(ax):
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, alpha=0.3)

    col_left, col_right = st.columns(2)

    # --- Temperatur ---
    with col_left:
        fig, ax = plt.subplots()
        ax.plot(df["time"], df["temperature_c"], label="Temperatur", color="tomato")
        ax.plot(df["time"], df["feels_like_c"], label="Føles som", color="tomato", linestyle="--", alpha=0.6)
        ax.set_title("Temperatur (°C)")
        ax.legend()
        fmt_xaxis(ax)
        st.pyplot(fig)
        plt.close(fig)

    # --- Vind ---
    with col_right:
        fig, ax = plt.subplots()
        ax.plot(df["time"], df["windspeed_kmh"], label="Vind", color="steelblue")
        ax.plot(df["time"], df["wind_gusts_kmh"], label="Vindstød", color="steelblue", linestyle="--", alpha=0.6)
        ax.set_title("Vind (km/t)")
        ax.legend()
        fmt_xaxis(ax)
        st.pyplot(fig)
        plt.close(fig)

    # --- Nedbør ---
    with col_left:
        fig, ax = plt.subplots()
        ax.bar(df["time"], df["precipitation_mm"], width=0.03, color="cornflowerblue", label="Nedbør (mm)")
        ax2 = ax.twinx()
        ax2.plot(df["time"], df["precipitation_probability_pct"], color="navy", linestyle="--", alpha=0.6, label="Sandsynlighed (%)")
        ax2.set_ylim(0, 100) # chance for regn i %
        ax.set_title("Nedbør")
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2)
        fmt_xaxis(ax)
        st.pyplot(fig)
        plt.close(fig)

    # --- UV ---
    with col_right:
        fig, ax = plt.subplots()
        ax.plot(df["time"], df["uv_index"], color="darkorange")
        ax.axhspan(3, 6, alpha=0.1, color="yellow", label="Moderat (3-6)")
        ax.axhspan(6, 11, alpha=0.1, color="orange", label="Høj (6+)")
        ax.set_title("UV-indeks")
        ax.legend()
        fmt_xaxis(ax)
        st.pyplot(fig)
        plt.close(fig)