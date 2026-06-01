lint:
	uv run ruff check .
 
format:
	uv run ruff format .
 
fix:
	ruff check . --fix
 
typecheck:
	uv run mypy .
 
test:
	uv run pytest
 
check: lint typecheck test
