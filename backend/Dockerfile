FROM ubuntu:noble-20250127

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
RUN uv --version

WORKDIR /project

COPY . .

RUN uv sync --no-dev
RUN uv pip install -e .

EXPOSE 8000


ENTRYPOINT ["uv", "run", "python","src/backend/entrypoints/webserver/run.py"]
