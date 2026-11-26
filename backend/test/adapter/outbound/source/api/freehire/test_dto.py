"""freehire DTO: 응답을 도메인으로 바꾸는 것과 검색 파라미터 검사.

HTTP는 쓰지 않음. freehire 약관상 실제 응답은 저장하지 않아서, detail_response.json은
명세(openapi.yaml)를 보고 지어낸 공고 하나 조회 응답.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from adapter.outbound.source.api.freehire.dto import (
    JOB_PAGE,
    FreehireJobDTO,
    FreehireSearchRequestDTO,
)

DETAIL = json.loads((Path(__file__).parent / "detail_response.json").read_text())


def test_search_request_needs_a_place():
    """도시도 나라도 없는 검색 파라미터는 거부한다.

    목적: 위치가 없으면 전 세계 공고를 찾아서 거의 항상 상한을 넘음.
    기대 결과: q만 → ValidationError. cities나 countries 하나만 있으면 통과.
    """
    with pytest.raises(ValidationError):
        FreehireSearchRequestDTO.model_validate({"q": "AI Engineer"})
    FreehireSearchRequestDTO.model_validate({"q": "AI Engineer", "cities": ["Berlin"]})
    FreehireSearchRequestDTO.model_validate({"q": "AI Engineer", "countries": ["de"]})


def test_search_request_rejects_unknown_keys():
    """DTO에 없는 키가 들어온 검색 파라미터는 거부한다.

    목적: Pydantic은 기본 설정에서 모르는 키를 조용히 버림.
    기대 결과: city(cities가 맞음) → ValidationError.
    """
    with pytest.raises(ValidationError):
        FreehireSearchRequestDTO.model_validate({"q": "AI Engineer", "city": ["Berlin"]})


def test_to_posting_turns_html_into_text_and_links_the_company_page():
    """공고 하나는 본문 HTML을 글자로 바꾸고, url은 회사 지원 페이지로 한다.

    목적: 본문은 HTML로 와서 태그가 LLM에게 그대로 감. 사용자는 회사 페이지에서 지원함.
    기대 결과: 문단 사이는 빈 줄, 목록 항목은 한 줄씩 "- "로, br은 줄바꿈, &amp;는 &.
    HTML 안의 줄바꿈 · 들여쓰기는 한 칸. url은 응답의 url.
    """
    job = FreehireJobDTO.model_validate(DETAIL["data"])
    posting = job.to_posting("freehire")

    assert posting.description == "We build agents.\n\n- Python & ML\n- LLMs\n\nApply\nnow"
    assert posting.url == DETAIL["data"]["url"]


def test_to_posting_links_the_freehire_page_without_a_company_page():
    """회사 지원 페이지가 없는 공고는 url을 freehire 공고 페이지로 한다.

    목적: freehire에서 바로 지원하는 공고는 응답의 url이 비어 있음 (명세의 direct_apply).
    기대 결과: url이 ""이면 JOB_PAGE/<public_slug>.
    """
    job = FreehireJobDTO.model_validate(DETAIL["data"] | {"url": ""})

    assert job.to_posting("freehire").url == f"{JOB_PAGE}/{job.public_slug}"


def test_to_summary_is_posting_without_url_and_description():
    """검색 결과용 변환(to_summary)은 to_posting에서 url과 본문만 뺀 것이다.

    목적: 검색 결과의 본문은 앞부분만 오는 미리보기라 버리고, LLM이 고른 공고만 get_job으로 채움.
    기대 결과: to_summary는 to_posting에서 url · description만 None.
    """
    job = FreehireJobDTO.model_validate(DETAIL["data"])

    assert job.to_summary("freehire") == job.to_posting("freehire").model_copy(
        update={"url": None, "description": None}
    )


def test_to_summary_lists_every_city():
    """근무지는 도시 목록(cities)이 있으면 그것을 쓰고, 없으면 location을 쓴다.

    목적: 근무지가 여러 곳인 공고는 location에 한 곳만 적히거나 비어 있음.
    기대 결과: cities ["Berlin", "Munich"] → "Berlin, Munich". cities가 없으면 location 그대로.
    """
    job = FreehireJobDTO.model_validate(
        DETAIL["data"] | {"location": "Berlin", "cities": ["Berlin", "Munich"]}
    )
    assert job.to_summary("freehire").location == "Berlin, Munich"
    assert (
        FreehireJobDTO.model_validate(DETAIL["data"]).to_summary("freehire").location
        == "Cambridge, UK"
    )
