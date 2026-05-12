.PHONY: backend frontend dev

backend:
	uv run uvicorn velo_weather.backend.main:app --reload

frontend:
	uv run streamlit run velo_weather/frontend/app.py

dev:
	make -j2 backend frontend