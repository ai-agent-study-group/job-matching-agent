"""/api 경로."""

from fastapi import APIRouter, Request

from adapter.inbound.agent.search import extract_jobs
from adapter.inbound.api.dto import SearchRequestDTO
from domain.job import JobPosting

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/api/search", response_model=list[JobPosting])
async def search(body: SearchRequestDTO, request: Request):
    profile_agent = request.app.state.profile_agent
    search_agent = request.app.state.search_agent
    # 이력서 분석 요청 (호출)
    profile = (await profile_agent.run(body.resume_text)).output
    # 채용공고 검색 요청 (호출)
    result = await search_agent.run(profile.model_dump_json())
    # 검색 결과 추출 및 HTTP 응답
    return extract_jobs(result)
