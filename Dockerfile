# 로컬 실행:
#   docker build -t jma:dev .
#   docker run --rm -p 8000:8000 jma:dev
#   curl localhost:8000/health   # {"status":"ok"}

# ---------------------------------------------------------------------------
# builder
# ---------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS builder

# uv는 pyproject.toml의 uv_build>=0.9.2,<0.10.0에 맞춰 0.9 계열을 씀.
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# 의존성 정의 파일만 먼저 복사 → 소스가 바뀌어도 이 레이어는 캐시에서 재사용됨.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# 소스 복사 후 프로젝트 자체(domain · port · service · adapter)를 설치
COPY . /app
RUN uv sync --locked --no-dev

# ---------------------------------------------------------------------------
# runtime
# ---------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runtime

# root로 실행하지 않음
RUN useradd --create-home --uid 10001 app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

# Railway · Render 같은 PaaS는 $PORT를 주입함. 없으면 8000을 씀.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import os,urllib.request;urllib.request.urlopen(f\"http://127.0.0.1:{os.environ.get('PORT','8000')}/health\")"

CMD ["sh", "-c", "uvicorn main:app --app-dir /app/src --host 0.0.0.0 --port ${PORT:-8000}"]
