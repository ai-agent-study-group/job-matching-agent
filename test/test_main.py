"""main.py 조립: 앱의 /mcp에 HTTP로 붙어 MCP 도구를 부름.

서버를 띄우지 않고 httpx2.ASGITransport로 앱에 바로 요청을 보냄.
출처 API를 부르는 도구(get_usage · search_jobs · get_job)는 부르지 않아서 네트워크를 쓰지 않음.
"""

import asyncio

import httpx2
import pytest
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from main import app


@pytest.fixture(autouse=True)
def llm_model(monkeypatch):
    # lifespan이 agent를 만들 때 LLM_MODEL을 읽음. "test"는 실제 LLM을 부르지 않는 pydantic-ai 시험용 모델
    monkeypatch.setenv("LLM_MODEL", "test")


def run(check):
    """앱의 lifespan을 돌리고 /mcp에 클라이언트를 붙여 check(client)를 돌린다."""

    def asgi_client(**kwargs):
        return httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), **kwargs)

    async def main():
        transport = StreamableHttpTransport("http://test/mcp", httpx_client_factory=asgi_client)
        async with app.router.lifespan_context(app), Client(transport) as client:
            return await check(client)

    return asyncio.run(main())


def test_mcp_over_http_lists_four_tools():
    """앱의 /mcp로 도구 네 개가 보인다.

    목적: claude.ai · ChatGPT 커넥터는 HTTP 주소로만 붙음.
    기대 결과: list_sources · get_usage · search_jobs · get_job.
    """
    tools = run(lambda client: client.list_tools())

    assert {t.name for t in tools} == {"list_sources", "get_usage", "search_jobs", "get_job"}


def test_mcp_over_http_list_sources():
    """list_sources가 main.py에서 조립한 출처 이름을 돌려준다.

    목적: 배포된 앱에서 어떤 출처를 쓸 수 있는지 확인.
    기대 결과: 연방고용청과 freehire.
    """
    result = run(lambda client: client.call_tool("list_sources", {}))

    names = [source["name"] for source in result.structured_content["result"]]
    assert names == ["arbeitsagentur", "freehire"]
