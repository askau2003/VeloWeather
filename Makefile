lint:
	uv run ruff check velo_weather
 
format:
	uv run ruff format velo_weather
 
typecheck:
	uv run mypy velo_weather
 
test:
	uv run pytest
 
check: lint typecheck test
