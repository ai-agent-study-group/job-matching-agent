"""ArbeitsagenturClient: 보내는 요청의 모양과 응답 처리.

실제 API 대신 fake_api가 정해 둔 응답(또는 요청마다 만든 응답)을 돌려주고, 보낸 요청을 기록함.
각 테스트는 실제 API를 불러서 알아낸 동작 중, 틀려도 오류 없이 결과만 틀려지는 것을 지킴.
"""

import asyncio
import json
from collections.abc import Callable
from pathlib import Path

import httpx2
import pytest

from adapter.outbound.source.api.arbeitsagentur.client import MAX_POSTINGS, ArbeitsagenturClient
from domain.job import JobPosting

SEARCH = json.loads((Path(__file__).parent / "search_response.json").read_text())
DETAIL = json.loads((Path(__file__).parent / "detail_response.json").read_text())


def fake_api(
    monkeypatch: pytest.MonkeyPatch,
    body: dict | Callable[[httpx2.Request], dict],
    status: int = 200,
) -> list[httpx2.Request]:
    """실제 API 대신 모든 요청에 body를 돌려주고, 보낸 요청 목록을 돌려준다.

    body가 함수면 요청마다 body(request)를 돌려준다. 응답 코드는 status.
    """
    sent = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(request)
        return httpx2.Response(status, json=body(request) if callable(body) else body)

    real = httpx2.AsyncClient
    monkeypatch.setattr(
        httpx2, "AsyncClient", lambda **kw: real(transport=httpx2.MockTransport(handler), **kw)
    )
    return sent


def test_search_sends_one_request_per_keyword_and_place(monkeypatch):
    """search가 키워드 × 위치 조합마다 올바른 요청을 하나씩 보낸다.

    목적: API는 요청 하나에 키워드 하나, 위치 하나만 받고 값 형식이 까다로움.
    기대 결과 (키워드 2개 × 위치 2개, arbeitszeit ["vz", "tz"]):
    - (was, wo) 조합마다 하나씩 요청 4개
    - 모든 요청에 arbeitszeit가 "vz;tz"
    - angebotsart처럼 넣지 않은 필터는 보내지 않음
    - 모든 요청에 size가 상한 + 1
    - 가짜 응답 4개에 반복된 공고 2건이 한 번씩만, 저장한 응답의 값 그대로 JobPosting으로 반환됨
    """
    sent = fake_api(monkeypatch, SEARCH)

    postings = asyncio.run(
        ArbeitsagenturClient().search(
            {
                "keywords": ["AI Engineer", "ML Engineer"],
                "locations": ["München", "Berlin"],
                "arbeitszeit": ["vz", "tz"],
            }
        )
    )

    queries = [dict(request.url.params) for request in sent]
    # 키워드나 위치를 공백으로 이으면 결과가 줄거나 도시가 버려짐
    assert sorted((q["was"], q["wo"]) for q in queries) == [
        ("AI Engineer", "Berlin"),
        ("AI Engineer", "München"),
        ("ML Engineer", "Berlin"),
        ("ML Engineer", "München"),
    ]
    # 목록은 ";"로 이어야 함 (같은 키를 반복하면 오류 없이 0건)
    assert all(q["arbeitszeit"] == "vz;tz" for q in queries)
    # 넣지 않은 필터는 보내지 않아야 함 (빈 값은 400)
    assert all("angebotsart" not in q for q in queries)
    # 상한보다 1건 더 받아야 넘었는지 알 수 있음
    assert all(q["size"] == str(MAX_POSTINGS + 1) for q in queries)
    assert len(postings) == len(SEARCH["ergebnisliste"])
    assert postings[0] == JobPosting(
        source="arbeitsagentur",
        id="12336-a26f1192j0456062-S",
        company="EXXETA AG",
        title="AI Engineer (m/d/w)",
        location="München",
    )


def test_search_merges_places_of_the_same_posting(monkeypatch):
    """같은 공고가 여러 지명 검색에 나오면 근무지를 합쳐 한 건으로 돌려준다.

    목적: 검색 목록은 공고의 근무지 중 검색한 지명과 맞는 곳 하나만 보여 줌. 근무지가 여러 곳인
    공고는 지명마다 나오는데, 하나만 남기면 마지막으로 검색한 지명의 도시만 남음.
    기대 결과: München · Berlin 검색에 같은 참조번호 → 공고 1건, location "München, Berlin".
    """

    def by_place(request: httpx2.Request) -> dict:
        place = {"adresse": {"ort": request.url.params["wo"]}}
        job = {"referenznummer": "1", "stellenangebotsTitel": "AI Engineer"}
        return {"ergebnisliste": [job | {"stellenlokationen": [place]}]}

    fake_api(monkeypatch, by_place)

    postings = asyncio.run(
        ArbeitsagenturClient().search(
            {"keywords": ["AI Engineer"], "locations": ["München", "Berlin"]}
        )
    )

    assert [p.location for p in postings] == ["München, Berlin"]


def test_search_asks_to_narrow_when_one_search_has_too_many(monkeypatch):
    """키워드 × 지명 조합 하나의 공고가 상한을 넘으면 오류를 낸다.

    목적: 상한까지만 받아서 주면 LLM은 결과가 잘린 줄 모름.
    기대 결과: 응답이 상한 + 1건(요청한 만큼 꽉 참) → 범위를 좁혀 다시 부르라는 ValueError.
    """
    jobs = [
        {"referenznummer": str(i), "stellenangebotsTitel": "Softwareentwickler"}
        for i in range(MAX_POSTINGS + 1)
    ]
    fake_api(monkeypatch, {"ergebnisliste": jobs})

    with pytest.raises(ValueError, match="Narrow the search"):
        asyncio.run(ArbeitsagenturClient().search({"keywords": ["Softwareentwickler"]}))


def test_search_asks_to_narrow_when_merged_postings_exceed_limit(monkeypatch):
    """조합마다는 상한 이하여도, 합친 공고가 상한을 넘으면 오류를 낸다.

    목적: 상한은 LLM에게 한 번에 가는 양을 막으려는 것이라 조합 하나가 아니라 결과 전체에 걸림.
    기대 결과: München · Berlin이 서로 다른 공고를 상한의 절반 + 1건씩 → ValueError.
    """
    half = MAX_POSTINGS // 2 + 1

    def by_place(request: httpx2.Request) -> dict:
        place = request.url.params["wo"]
        jobs = [
            {"referenznummer": f"{place}-{i}", "stellenangebotsTitel": "AI Engineer"}
            for i in range(half)
        ]
        return {"ergebnisliste": jobs}

    fake_api(monkeypatch, by_place)

    with pytest.raises(ValueError, match="Narrow the search"):
        asyncio.run(
            ArbeitsagenturClient().search(
                {"keywords": ["AI Engineer"], "locations": ["München", "Berlin"]}
            )
        )


def test_search_fails_on_unknown_place(monkeypatch):
    """API가 모르는 지명이면 search가 오류를 낸다.

    목적: API는 모르는 지명(예: Munich)에 오류 없이 0건으로 답해서, LLM이 München으로
    다시 부르지 않고 "공고 없음"으로 답하게 됨.
    기대 결과: API가 Munich에 실제로 돌려주는 응답일 때, 지명이 들어간 ValueError.
    """
    fake_api(monkeypatch, {"maxErgebnisse": 0, "woOutput": {"suchmodus": "UNGUELTIG"}})

    with pytest.raises(ValueError, match="Munich"):
        asyncio.run(
            ArbeitsagenturClient().search({"keywords": ["AI Engineer"], "locations": ["Munich"]})
        )


def test_fetch_sends_reference_number_in_base64(monkeypatch):
    """fetch가 참조번호를 base64로 바꿔 상세 주소로 보낸다.

    목적: 상세 조회 주소는 참조번호를 그대로가 아니라 base64로 받음.
    기대 결과: 요청 주소가 /pc/v4/jobdetails/<base64(참조번호)>이고, 본문까지 채운 JobPosting이 돌아옴.
    """
    sent = fake_api(monkeypatch, DETAIL)

    posting = asyncio.run(ArbeitsagenturClient().fetch("13509-000021100c7004-S"))

    assert sent[0].url.path.endswith("/pc/v4/jobdetails/MTM1MDktMDAwMDIxMTAwYzcwMDQtUw==")
    assert posting.description == DETAIL["stellenangebotsBeschreibung"]


def test_fetch_fails_on_unknown_id(monkeypatch):
    """없는 참조번호면 fetch가 그 참조번호가 든 오류를 낸다.

    목적: API는 없는 참조번호에 404로 답함. 그대로 두면 LLM에게 base64 주소와 HTTP 설명 링크가
    든 오류가 가서 무엇이 틀렸는지 읽기 어려움.
    기대 결과: API가 404를 돌려줄 때, 참조번호가 들어간 ValueError.
    """
    fake_api(monkeypatch, {}, status=404)

    with pytest.raises(ValueError, match="99999-0000000000-S"):
        asyncio.run(ArbeitsagenturClient().fetch("99999-0000000000-S"))
