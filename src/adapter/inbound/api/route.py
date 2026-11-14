"""/api 경로."""

from fastapi import APIRouter, HTTPException, Request
from fastmcp import Client

from adapter.inbound.agent.search import extract_jobs
from adapter.inbound.api.dto import JDRequestDTO, SearchRequestDTO
from domain.jd import JD
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


@router.post("/api/jd", response_model=JD)
async def summarize_job(body: JDRequestDTO, request: Request) -> JD:
    """Fetch a job posting and extract structured JD."""

    # 1. MCP get_job 호출
    async with Client(request.app.state.mcp_server) as client:
        response = await client.call_tool(
            "get_job",
            {
                "source": body.source,
                "posting_id": body.posting_id,
            },
            raise_on_error=False,
        )

    # 2. 상세 조회 오류 처리
    if response.is_error:
        error_text = " ".join(getattr(part, "text", "") for part in response.content)
        if "Unknown source" in error_text:
            raise HTTPException(status_code=400, detail=error_text)
        if "No posting with id" in error_text or "is closed" in error_text:
            raise HTTPException(status_code=404, detail=error_text)
        raise HTTPException(status_code=502, detail="Failed to fetch job")

    # 3. MCP 응답을 JobPosting으로 변환
    job = JobPosting.model_validate(response.structured_content)

    if job.source != body.source or job.id != body.posting_id:
        raise HTTPException(status_code=502, detail="Unexpected job returned")

    # 4. 공고 본문 검증
    if not job.description or not job.description.strip():
        raise HTTPException(status_code=422, detail="Job description is empty")

    # 5. Job Summarizer Agent 실행
    agent = request.app.state.job_summarizer_agent
    result = await agent.run(job.model_dump_json())

    # 6. 원본 메타데이터 유지 및 JD 반환
    return result.output.model_copy(
        update={
            "source": job.source,
            "posting_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
        }
    )
