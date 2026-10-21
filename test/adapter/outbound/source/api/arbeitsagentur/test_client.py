"""ArbeitsagenturClient: 보내는 요청의 모양과 응답 처리.

실제 API 대신 fake_api가 모든 요청에 정해 둔 응답을 돌려주고, 보낸 요청을 기록함.
각 테스트는 실제 API를 불러서 알아낸 동작 중, 틀려도 오류 없이 결과만 틀려지는 것을 지킴.
"""

import asyncio
import json
from pathlib import Path

import httpx2
import pytest

from adapter.outbound.source.api.arbeitsagentur.client import ArbeitsagenturClient

SEARCH = json.loads((Path(__file__).parent / "search_response.json").read_text())


def fake_api(monkeypatch: pytest.MonkeyPatch, body: dict) -> list[httpx2.Request]:
    """실제 API 대신 모든 요청에 body를 돌려주고, 보낸 요청 목록을 돌려준다."""
    sent = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        sent.append(request)
        return httpx2.Response(200, json=body)

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
    - 가짜 응답 4개에 반복된 공고 2건이 한 번씩만 반환됨
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
    assert len(postings) == len(SEARCH["ergebnisliste"])


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
