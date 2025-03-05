FROM ubuntu:noble-20250127

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
RUN uv --version

WORKDIR /frontend

COPY . .
RUN uv sync --no-dev
RUN uv pip install -e .

ENTRYPOINT  [ "uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8005" ]