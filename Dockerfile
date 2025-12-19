FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv export --format=requirements-txt --no-dev > requirements.txt && \
    uv pip install --system --no-cache -r requirements.txt

COPY . .

CMD ["python", "-m", "src.main"]