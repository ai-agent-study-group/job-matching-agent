"""/api 경로."""

from typing import Annotated

from fastapi import APIRouter, File, Request
from pydantic_ai.exceptions import AgentRunError

from adapter.inbound.agent.search import extract_jobs
from adapter.inbound.api.document_parser import document_to_text
from adapter.inbound.api.dto import ProfileRequestDTO
from adapter.inbound.api.error import agent_error, agent_errors, resume_file_errors
from domain.job import JobPosting
from domain.profile import Profile

# operationId를 함수 이름으로 씀. FE TS 타입의 이름이 search_api_search_post 대신 search가 됨
router = APIRouter(generate_unique_id_function=lambda route: route.name)


@router.get("/health", tags=["system"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/api/profile",
    tags=["profile"],
    summary="Extract a profile from a resume",
    responses={
        **resume_file_errors(),
        **agent_errors("Profile extraction failed"),
    },
)
async def profile(body: Annotated[ProfileRequestDTO, File()], request: Request) -> Profile:
    """Extract experience, education, skills and languages from the resume.

    Send the resume in the `resume` form field, as plain text or as a PDF or DOCX file.
    A file with no extractable text is rejected with 422 and a one-sentence `detail`.
    """
    resume = body.resume
    text = resume if isinstance(resume, str) else await document_to_text(resume)
    try:
        result = await request.app.state.profile_agent.run(text)
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
