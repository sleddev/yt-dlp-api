# Use the official Deno image as a source for the binary
FROM denoland/deno:bin AS deno_bin
FROM python:3.14-slim

# 1. Install System Dependencies (Solver and Deno requirements)
# We add 'glpk-utils' as a common solver, but you can swap it for 'coinor-cbc' or others.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    glpk-utils \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy Deno binary from the first stage
COPY --from=deno_bin /deno /usr/local/bin/deno

# Setup uv (your existing setup)
RUN pip install --no-cache-dir uv
WORKDIR /app

# 3. Add EJS and Solver to your Python environment
# Assuming 'ejs' refers to the Python-based ejs-template or similar.
# If you meant the JavaScript EJS, you'd use 'deno install' instead.
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev
RUN uv add ejs-template  # Or manually add to pyproject.toml

COPY . .
RUN mkdir -p downloads

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]