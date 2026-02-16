FROM python:3.14-slim

RUN pip install --no-cache-dir uv

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl unzip && \
    rm -rf /var/lib/apt/lists/*

RUN sh -c "curl -fsSL https://deno.land/install.sh | sh"

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-dev

COPY . .

RUN mkdir -p downloads

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
