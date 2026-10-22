"""MCP 서버: 등록한 도구와 부른 결과.

서버를 띄우지 않고 메모리 안 클라이언트(fastmcp.Client)로 바로 붙음.
출처는 정해 둔 공고만 돌려주는 FakeSource라서 네트워크를 쓰지 않음.
"""

import asyncio

from fastmcp import Client
from pydantic import BaseModel, ConfigDict

from adapter.inbound.mcp.server import create_server
from domain.job import JobPosting
from port.outbound.source import JobSource
from service.job import JobService

POSTING = JobPosting(
    source="fake",
    id="1",
    company="ACME",
    title="AI Engineer",
    location="München",
    url="https://example.com/1",
)


class FakeRequestDTO(BaseModel):
    """가짜 출처의 검색 조건 형식."""

    model_config = ConfigDict(extra="forbid")

    keywords: list[str]


class FakeSource(JobSource):
    """HTTP 없이 POSTING만 돌려주는 출처."""

    async def usage(self) -> type[BaseModel]:
        return FakeRequestDTO

    async def search(self, params: dict) -> list[JobPosting]:
        FakeRequestDTO.model_validate(params)
        return [POSTING]

    async def fetch(self, posting_id: str) -> JobPosting:
        return POSTING


def run(check):
    """FakeSource를 넣은 서버에 클라이언트를 붙여 check(client)를 돌린다."""

    async def main():
        async with Client(create_server(JobService(FakeSource()))) as client:
            return await check(client)

    return asyncio.run(main())


def test_three_tools_registered_read_only():
    """도구 세 개가 읽기 전용으로 등록된다.

    목적: MCP 클라이언트는 서버가 알려 준 도구 목록만 보고 부름.
    기대 결과: get_usage · search_jobs · get_job이 있고, 모두 readOnlyHint가 True.
    """
    tools = run(lambda client: client.list_tools())

    assert {t.name for t in tools} == {"get_usage", "search_jobs", "get_job"}
    assert all(t.annotations.read_only_hint for t in tools)


def test_search_jobs_returns_postings():
    """search_jobs를 부르면 출처가 돌려준 공고가 그대로 온다.

    목적: 서버 · 서비스를 거치면서 공고가 바뀌거나 빠지지 않는지 확인.
    기대 결과: 결과가 {"result": [POSTING]}과 같음.
    """
    # call_tool(도구 이름, 도구 인자 {인자 이름: 값}). search_jobs의 인자는 params 하나
    result = run(
        lambda client: client.call_tool("search_jobs", {"params": {"keywords": ["AI Engineer"]}})
    )

    assert result.structured_content == {"result": [POSTING.model_dump()]}
