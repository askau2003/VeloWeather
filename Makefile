.PHONY: backend frontend dev

backend:
	uv run uvicorn velo_weather.backend.main:app \
		--reload \
		--reload-dir velo_weather

frontend:
	uv run streamlit run velo_weather/frontend/app.py \
		--server.runOnSave true

dev:
	make -j2 backend frontend