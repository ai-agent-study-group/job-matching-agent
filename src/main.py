"""조립: 어댑터를 service에 연결하고 /api와 /mcp를 한 FastAPI 앱에 올림."""

from fastapi import FastAPI

from adapter.inbound.api.route import router as api_router

app = FastAPI(title="job-matching-agent API")
app.include_router(api_router)
