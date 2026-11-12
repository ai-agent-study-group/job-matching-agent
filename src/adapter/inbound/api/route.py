"""/api 경로."""

from fastapi import APIRouter, Request
from pydantic_ai.exceptions import AgentRunError

from adapter.inbound.agent.search import extract_jobs
from adapter.inbound.api.dto import ProfileRequestDTO
from adapter.inbound.api.error import agent_error, agent_errors
from domain.job import JobPosting
from domain.profile import Profile

# operationId를 함수 이름으로 씀. FE TS 타입의 이름이 search_api_search_post 대신 search가 됨
router = APIRouter(generate_unique_id_function=lambda route: route.name)


@router.get("/health", tags=["system"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/api/profile",
    response_model=Profile,
    tags=["profile"],
    summary="Extract a profile from a resume",
    responses=agent_errors("Profile extraction failed"),
)
async def profile(body: ProfileRequestDTO, request: Request):
    """Extract job titles and preferred work locations from the resume text."""
    try:
        result = await request.app.state.profile_agent.run(body.resume_text)
    except AgentRunError as e:
        raise agent_error(e, "Profile extraction failed") from e
    return result.output


@router.post(
    "/api/search",
    response_model=list[JobPosting],
    tags=["search"],
    summary="Search job postings for a profile",
    responses=agent_errors("Job search failed"),
)
async def search(body: Profile, request: Request):
    """Search the job sources through the MCP tools for postings that match the profile.

    Pass the profile returned by /api/profile, edited by the user if needed.
    """
    try:
        result = await request.app.state.search_agent.run(body.model_dump_json())
    except AgentRunError as e:
        raise agent_error(e, "Job search failed") from e
    return extract_jobs(result)
