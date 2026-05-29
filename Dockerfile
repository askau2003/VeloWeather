FROM python:3.14

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv pip install --system .

COPY . .