"""FreehireClient: 보내는 요청의 모양과 응답 처리.

실제 API 대신 fake_api가 정해 둔 응답을 돌려주고, 보낸 요청을 기록함.
freehire 약관상 실제 응답은 저장하지 않아서, search_response.json · detail_response.json은
명세(openapi.yaml)를 보고 지어낸 응답. 검색 응답은 이름이 같은 영국 · 미국 Cambridge 공고 2건.
"""

import asyncio
import json
from pathlib import Path

import httpx2
import pytest

from adapter.outbound.source.api.freehire.client import MAX_POSTINGS, FreehireClient
from adapter.outbound.source.api.freehire.dto import JOB_PAGE
from domain.job import JobPosting

SEARCH = json.loads((Path(__file__).parent / "search_response.json").read_text())
DETAIL = json.loads((Path(__file__).parent / "detail_response.json").read_text())


def fake_api(
    monkeypatch: pytest.MonkeyPatch, body: dict, status: int = 200
) -> list[httpx2.Request]:
    """실제 API 대신 모든 요청에 body를 돌려주고, 보낸 요청 목록을 돌려준다."""
    sent = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(request)
        return httpx2.Response(status, json=body)

    real = httpx2.AsyncClient
    monkeypatch.setattr(
        httpx2, "AsyncClient", lambda **kw: real(transport=httpx2.MockTransport(handler), **kw)
    )
    return sent


def search(params: dict) -> list[JobPosting]:
    return asyncio.run(FreehireClient().search(params))


def test_search_sends_filters_in_the_api_format(monkeypatch):
    """search가 검색 파라미터를 API가 받는 모양으로 보낸다.

    목적: 모양이 틀려도 API는 오류 없이 다르게 검색함.
    기대 결과:
    - 목록은 같은 키를 반복 (cities=Cambridge&cities=Oxford)
    - q_fields만 쉼표로 이은 글자 하나
    - 넣지 않은 필터는 보내지 않음
    - limit은 상한
    - 응답 공고 2건이 응답의 값 그대로 JobPosting으로 반환됨
    """
    sent = fake_api(monkeypatch, SEARCH)

    postings = search(
        {"q": "AI Engineer", "q_fields": ["title", "company"], "cities": ["Cambridge", "Oxford"]}
    )

    params = sent[0].url.params
    assert params.get_list("cities") == ["Cambridge", "Oxford"]
    assert params["q_fields"] == "title,company"
    assert "work_mode" not in params
    assert params["limit"] == str(MAX_POSTINGS)
    assert postings == [
        JobPosting(
            source="freehire",
            id="ai-engineer-acme-cambridge",
            company="Acme",
            title="AI Engineer",
            location="Cambridge, UK",
        ),
        JobPosting(
            source="freehire",
            id="ml-engineer-globex-cambridge",
            company="Globex",
            title="ML Engineer",
            location="Cambridge, MA",
        ),
    ]


def test_search_with_cities_and_countries_keeps_only_those_countries(monkeypatch):
    """도시와 나라가 같이 오면 도시로만 찾고, 받은 공고를 나라로 거른다.

    목적: API는 위치를 OR로 묶어서, 나라를 같이 보내면 그 나라 전체가 나옴.
    기대 결과: 요청에 countries가 없고, 영국(gb) 공고만 남음 (같은 이름의 미국 도시 공고는 빠짐).
    나라 코드를 대문자 GB로 줘도 같음.
    """
    sent = fake_api(monkeypatch, SEARCH)

    postings = search({"q": "AI Engineer", "cities": ["Cambridge"], "countries": ["GB"]})

    assert "countries" not in sent[0].url.params
    assert [p.location for p in postings] == ["Cambridge, UK"]


def test_search_asks_to_narrow_when_total_exceeds_limit(monkeypatch):
    """검색된 공고 수가 상한을 넘으면 오류를 낸다.

    목적: 상한까지만 받아서 주면 LLM은 결과가 잘린 줄 모름.
    기대 결과: meta.total이 상한 + 1 → 범위를 좁혀 다시 부르라는 ValueError.
    """
    fake_api(monkeypatch, {"data": [], "meta": {"total": MAX_POSTINGS + 1}})

    with pytest.raises(ValueError, match="Narrow the search"):
        search({"q": "Engineer", "countries": ["de"]})


def test_search_fails_when_freehire_ignores_part_of_it(monkeypatch):
    """API가 파라미터나 값을 무시했다고 알려 오면 오류를 낸다.

    목적: API는 모르는 파라미터를 버리고, 허용 목록 밖 값은 0건으로 오류 없이 답함.
    그대로 두면 LLM이 "공고 없음"으로 답함.
    기대 결과: meta.ignored_values가 있으면 그 값이 들어간 ValueError.
    """
    meta = {"total": 0, "ignored_values": {"countries": ["xx"]}}
    fake_api(monkeypatch, {"data": [], "meta": meta})

    with pytest.raises(ValueError, match="xx"):
        search({"q": "AI Engineer", "countries": ["xx"]})


def test_search_passes_on_the_reason_of_a_bad_request(monkeypatch):
    """API가 400으로 답하면 API가 준 이유를 오류로 낸다.

    목적: 그대로 두면 LLM에게 주소와 HTTP 설명 링크가 든 오류가 가서 무엇이 틀렸는지 모름.
    기대 결과: {"error": "..."} 400 → 그 메시지가 든 ValueError.
    """
    fake_api(monkeypatch, {"error": "at most 5 OR alternatives"}, status=400)

    with pytest.raises(ValueError, match="at most 5 OR alternatives"):
        search({"q": "a OR b OR c OR d OR e OR f", "countries": ["de"]})


def test_requests_share_one_client(monkeypatch):
    """요청들은 어댑터를 만들 때 만든 클라이언트 하나를 같이 쓴다.

    목적: 요청마다 클라이언트를 만들고 닫으면 맺어 둔 연결도 버려져서, 매번 새로 연결함.
    기대 결과: 검색을 두 번 해도 처음 만든 클라이언트가 그대로 있고, 닫히지 않음.
    """
    sent = fake_api(monkeypatch, {"data": [], "meta": {"total": 0}})
    source = FreehireClient()
    http = source.http

    async def main():
        await source.search({"q": "AI Engineer", "countries": ["de"]})
        await source.search({"q": "ML Engineer", "countries": ["de"]})

    asyncio.run(main())

    assert len(sent) == 2
    assert source.http is http
    assert not http.is_closed


def test_fetch_escapes_the_id_in_the_path(monkeypatch):
    """fetch가 id를 주소에 넣을 때 "/" 같은 글자를 바꿔 넣는다.

    목적: id는 LLM이 넘기는 값이라, 그대로 넣으면 "../companies" 같은 id로 다른 주소를 부를 수 있음.
    기대 결과: 요청 주소가 /api/v1/jobs/..%2Fcompanies.
    """
    sent = fake_api(monkeypatch, DETAIL)

    asyncio.run(FreehireClient().fetch("../companies"))

    assert sent[0].url.raw_path.decode() == "/api/v1/jobs/..%2Fcompanies"


def test_fetch_returns_the_posting_with_its_freehire_page(monkeypatch):
    """fetch가 공고 하나를 freehire 공고 페이지 링크와 본문까지 채워 돌려준다.

    기대 결과: url이 JOB_PAGE/<id>, 본문은 HTML 태그가 빠진 글자.
    """
    fake_api(monkeypatch, DETAIL)

    posting = asyncio.run(FreehireClient().fetch("ai-engineer-acme-cambridge"))

    assert posting.url == f"{JOB_PAGE}/ai-engineer-acme-cambridge"
    assert posting.description.startswith("We build agents.")


def test_fetch_fails_on_unknown_id(monkeypatch):
    """없는 공고 id면 fetch가 그 id가 든 오류를 낸다.

    목적: API는 없는 id에 404로 답함. 그대로 두면 HTTP 설명 링크가 든 오류가 감.
    기대 결과: API가 404를 돌려줄 때, id가 들어간 ValueError.
    """
    fake_api(monkeypatch, {"error": "not found"}, status=404)

    with pytest.raises(ValueError, match="no-such-job"):
        asyncio.run(FreehireClient().fetch("no-such-job"))


def test_fetch_fails_on_closed_posting(monkeypatch):
    """마감된 공고면 fetch가 오류를 낸다.

    목적: 공고 하나 조회는 마감된 공고도 돌려줘서, 그대로 두면 LLM이 마감된 공고를 추천할 수 있음.
    기대 결과: closed_at이 있으면 ValueError.
    """
    closed = DETAIL["data"] | {"closed_at": "2026-10-01T00:00:00Z"}
    fake_api(monkeypatch, {"data": closed})

    with pytest.raises(ValueError, match="closed"):
        asyncio.run(FreehireClient().fetch("ai-engineer-acme-cambridge"))
