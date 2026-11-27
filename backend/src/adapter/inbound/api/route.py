"""/api 경로."""

from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, status
from pydantic_ai.exceptions import AgentRunError

from adapter.inbound.agent.search import extract_jobs
from adapter.inbound.api.dto import ErrorDTO, ProfileRequestDTO
from adapter.inbound.api.error import agent_error, agent_errors
from domain.job import JobPosting
from domain.profile import Profile

# operationId를 함수 이름으로 씀. FE TS 타입의 이름이 search_api_search_post 대신 search가 됨
router = APIRouter(generate_unique_id_function=lambda route: route.name)

RESUME_FILE_UNSUPPORTED = "Resume files are not supported yet. Send the resume as text"


@router.get("/health", tags=["system"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/api/profile",
    tags=["profile"],
    summary="Extract a profile from a resume",
    responses={
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {
            "model": ErrorDTO,
            "description": RESUME_FILE_UNSUPPORTED,
        },
        **agent_errors("Profile extraction failed"),
    },
)
async def profile(body: Annotated[ProfileRequestDTO, File()], request: Request) -> Profile:
    """Extract experience, education, skills and languages from the resume.

    Send the resume in the `resume` form field, as plain text or as a file.
    """
    # 파일을 텍스트로 바꾸는 부분은 #44에서 붙임. 그때까지 파일은 받지 않음
    if not isinstance(body.resume, str):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, RESUME_FILE_UNSUPPORTED)
    try:
        result = await request.app.state.profile_agent.run(body.resume)
    except AgentRunError as e:
        raise agent_error(e, "Profile extraction failed") from e
    return result.output


@router.post(
    "/api/search",
    tags=["search"],
    summary="Search job postings for a profile",
    responses=agent_errors("Job search failed"),
)
async def search(body: Profile, request: Request) -> list[JobPosting]:
    """Search the job sources through the MCP tools for postings that match the profile.

    Pass the profile returned by /api/profile. Unknown fields are rejected with 422.
    """
    try:
        result = await request.app.state.search_agent.run(body.model_dump_json())
    except AgentRunError as e:
        raise agent_error(e, "Job search failed") from e
    return extract_jobs(result)
