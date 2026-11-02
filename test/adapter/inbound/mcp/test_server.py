"""MCP 서버: 등록한 도구와 부른 결과.

서버를 띄우지 않고 메모리 안 클라이언트(fastmcp.Client)로 바로 붙음.
출처는 정해 둔 공고만 돌려주는 가짜 두 개(FakeSource · OtherSource)라서 네트워크를 쓰지 않음.
"""

import asyncio

import pytest
from fastmcp import Client
from pydantic import BaseModel, ConfigDict

from adapter.inbound.mcp.server import create_server
from domain.job import JobPosting
from port.outbound.source import JobSource
from service.job import JobService
from service.registry import RegistryService

POSTING = JobPosting(
    source="fake",
    id="1",
    company="ACME",
    title="AI Engineer",
    location="München",
    url="https://example.com/1",
)
# 다른 출처의 공고. id가 POSTING과 같음
OTHER_POSTING = POSTING.model_copy(update={"source": "other", "company": "Globex"})


class FakeRequestDTO(BaseModel):
    """가짜 출처의 검색 조건 형식."""

    model_config = ConfigDict(extra="forbid")

    keywords: list[str]


class FakeSource(JobSource):
    """HTTP 없이 POSTING만 돌려주는 출처."""

    def name(self) -> str:
        return "fake"

    def description(self) -> str:
        return "Fake postings"

    async def usage(self) -> type[BaseModel]:
        return FakeRequestDTO

    async def search(self, params: dict) -> list[JobPosting]:
        FakeRequestDTO.model_validate(params)
        return [POSTING]

    async def fetch(self, posting_id: str) -> JobPosting:
        return POSTING


class OtherRequestDTO(BaseModel):
    """다른 출처의 검색 조건 형식."""

    q: str


class OtherSource(FakeSource):
    """검색 조건과 공고가 FakeSource와 다른 출처."""

    def name(self) -> str:
        return "other"

    def description(self) -> str:
        return "Other postings"

    async def usage(self) -> type[BaseModel]:
        return OtherRequestDTO

    async def fetch(self, posting_id: str) -> JobPosting:
        return OTHER_POSTING


def run(check):
    """가짜 출처 두 개를 넣은 서버에 클라이언트를 붙여 check(client)를 돌린다."""

    async def main():
        registry = RegistryService([JobService(FakeSource()), JobService(OtherSource())])
        async with Client(create_server(registry)) as client:
            return await check(client)

    return asyncio.run(main())


def test_four_tools_registered_read_only():
    """도구 네 개가 읽기 전용으로 등록된다.

    목적: MCP 클라이언트는 서버가 알려 준 도구 목록만 보고 부름. 출처가 늘어도 도구는 그대로임.
    기대 결과: list_sources · get_usage · search_jobs · get_job이 있고, 모두 readOnlyHint가 True.
    """
    tools = run(lambda client: client.list_tools())

    assert {t.name for t in tools} == {"list_sources", "get_usage", "search_jobs", "get_job"}
    assert all(t.annotations.read_only_hint for t in tools)


def test_list_sources_returns_names_and_descriptions():
    """list_sources가 출처 어댑터에 적힌 이름과 설명을 돌려준다.

    목적: LLM은 설명을 보고 요청에 맞는 출처를 골라, 그 이름을 다른 도구에 넘김.
    기대 결과: 가짜 출처 두 개의 이름과 설명.
    """
    result = run(lambda client: client.call_tool("list_sources", {}))

    assert result.structured_content == {
        "result": [
            {"name": "fake", "description": "Fake postings"},
            {"name": "other", "description": "Other postings"},
        ]
    }


def test_sources_with_the_same_name_fail_at_assembly():
    """이름이 같은 출처를 둘 넣으면 조립할 때 오류가 난다.

    목적: 이름으로 출처를 찾아서, 겹치면 한 출처가 목록에서 조용히 사라짐.
    기대 결과: RegistryService를 만들 때 ValueError이고, 메시지에 겹친 이름이 들어 있음.
    """
    with pytest.raises(ValueError, match="fake, fake"):
        RegistryService([JobService(FakeSource()), JobService(FakeSource())])


def test_get_usage_returns_the_format_of_the_chosen_source():
    """get_usage가 고른 출처의 검색 조건 형식을 돌려준다.

    목적: 출처마다 검색 조건이 달라서, 다른 출처의 형식이 가면 LLM이 틀린 params를 보냄.
    기대 결과: fake는 keywords, other는 q.
    """
    fake = run(lambda client: client.call_tool("get_usage", {"source": "fake"}))
    other = run(lambda client: client.call_tool("get_usage", {"source": "other"}))

    assert "keywords" in fake.structured_content["properties"]
    assert "q" in other.structured_content["properties"]


def test_get_job_with_the_same_id_goes_to_the_chosen_source():
    """id가 같아도 get_job은 고른 출처의 공고를 돌려준다.

    목적: 공고 id는 출처마다 따로 발급해서, 출처가 달라도 같을 수 있음.
    기대 결과: 같은 id "1"로 fake는 POSTING, other는 OTHER_POSTING.
    """

    def get(source):
        args = {"source": source, "posting_id": "1"}
        return run(lambda client: client.call_tool("get_job", args)).structured_content

    assert get("fake") == POSTING.model_dump()
    assert get("other") == OTHER_POSTING.model_dump()


@pytest.mark.parametrize(
    ("tool", "args"),
    [
        pytest.param("get_usage", {}, id="get_usage"),
        pytest.param("search_jobs", {"params": {}}, id="search_jobs"),
        pytest.param("get_job", {"posting_id": "1"}, id="get_job"),
    ],
)
def test_unknown_source_tells_the_names(tool, args):
    """없는 출처 이름이면 고를 수 있는 이름이 오류로 온다.

    목적: LLM이 이름을 지어내도 오류를 보고 스스로 고치게 함.
    기대 결과: 오류이고, 메시지에 틀린 이름과 fake · other가 들어 있음.
    """
    result = run(
        lambda client: client.call_tool(tool, args | {"source": "nope"}, raise_on_error=False)
    )
    text = result.content[0].text

    assert result.is_error
    assert "nope" in text
    assert "fake, other" in text


def test_search_jobs_returns_postings():
    """search_jobs를 부르면 출처가 돌려준 공고가 그대로 온다.

    목적: 서버 · 서비스를 거치면서 공고가 바뀌거나 빠지지 않는지 확인.
    기대 결과: 결과가 {"result": [POSTING]}과 같음.
    """
    # call_tool(도구 이름, 도구 인자 {인자 이름: 값}). search_jobs의 인자는 source와 params
    args = {"source": "fake", "params": {"keywords": ["AI Engineer"]}}
    result = run(lambda client: client.call_tool("search_jobs", args))

    assert result.structured_content == {"result": [POSTING.model_dump()]}


@pytest.mark.parametrize(
    ("params", "wrong_key"),
    [
        pytest.param({"kw": ["AI Engineer"]}, "kw", id="unknown-key"),
        pytest.param(
            {"keywords": ["AI Engineer"], "location": "München"}, "location", id="extra-key"
        ),
        pytest.param({"keywords": "AI Engineer"}, "keywords", id="wrong-type"),
    ],
)
def test_search_jobs_bad_params_tells_wrong_key_and_get_usage(params, wrong_key):
    """params가 틀리면 틀린 키와 get_usage를 부르라는 안내가 오류로 온다.

    목적: LLM이 params를 지어내거나 잘못 보내도 무엇이 틀렸는지 보고 스스로 고치게 함.
    기대 결과: 오류이고, 메시지에 틀린 키 이름과 "get_usage"가 들어 있음.
    """
    args = {"source": "fake", "params": params}
    result = run(lambda client: client.call_tool("search_jobs", args, raise_on_error=False))
    text = result.content[0].text

    assert result.is_error
    assert wrong_key in text
    assert "get_usage" in text
