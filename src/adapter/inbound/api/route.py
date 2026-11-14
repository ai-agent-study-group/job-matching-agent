"""/api 경로."""

from fastapi import APIRouter, Request

from adapter.inbound.agent.search import extract_jobs
from adapter.inbound.api.dto import SearchRequestDTO
from domain.job import JobPosting

# operationId를 함수 이름으로 씀. FE TS 타입의 이름이 search_api_search_post 대신 search가 됨
router = APIRouter(generate_unique_id_function=lambda route: route.name)


@router.get("/health", tags=["system"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/api/search",
    response_model=list[JobPosting],
    tags=["search"],
    summary="Search job postings for a resume",
)
async def search(body: SearchRequestDTO, request: Request):
    """Extract job titles and preferred locations from the resume text,
    then search the job sources through the MCP tools and return the postings found.
    """
    profile_agent = request.app.state.profile_agent
    search_agent = request.app.state.search_agent
    # 이력서 분석 요청 (호출)
    profile = (await profile_agent.run(body.resume_text)).output
    # 채용공고 검색 요청 (호출)
    result = await search_agent.run(profile.model_dump_json())
    # 검색 결과 추출 및 HTTP 응답
    return extract_jobs(result)
