import streamlit as st
import requests

st.title("My Streamlit App")

response = requests.get("http://localhost:8000/api/data")

data = response.json()

st.write(data)