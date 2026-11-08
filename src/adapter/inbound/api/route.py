"""/api 경로."""

from fastapi import APIRouter, Request

from adapter.inbound.agent.search import run_search_agent
from adapter.inbound.api.dto import SearchRequest
from domain.job import JobPosting

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/api/search", response_model=list[JobPosting])
async def search(body: SearchRequest, request: Request):
    profile_agent = request.app.state.profile_agent
    search_agent = request.app.state.search_agent

    profile = (await profile_agent.run(body.resume_text)).output

    return await run_search_agent(search_agent, profile)
