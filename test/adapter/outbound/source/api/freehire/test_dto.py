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


def test_to_posting_turns_html_into_text_and_links_the_freehire_page():
    """공고 하나는 본문 HTML을 글자로 바꾸고, url은 freehire 공고 페이지로 한다.

    목적: 본문은 HTML로 와서 태그가 LLM에게 그대로 감. 약관상 공고마다 freehire 링크가 필요함.
    기대 결과: 문단 사이는 빈 줄, 목록 항목은 한 줄씩 "- "로, br은 줄바꿈, &amp;는 &.
    HTML 안의 줄바꿈 · 들여쓰기는 한 칸. url은 JOB_PAGE/<public_slug>.
    """
    job = FreehireJobDTO.model_validate(DETAIL["data"])
    posting = job.to_posting()

    assert posting.description == "We build agents.\n\n- Python & ML\n- LLMs\n\nApply\nnow"
    assert posting.url == f"{JOB_PAGE}/{job.public_slug}"


def test_to_summary_is_posting_without_url_and_description():
    """검색 결과용 변환(to_summary)은 to_posting에서 url과 본문만 뺀 것이다.

    목적: 검색 결과의 본문은 앞부분만 오는 미리보기라 버리고, LLM이 고른 공고만 get_job으로 채움.
    기대 결과: to_summary는 to_posting에서 url · description만 None.
    """
    job = FreehireJobDTO.model_validate(DETAIL["data"])

    assert job.to_summary() == job.to_posting().model_copy(
        update={"url": None, "description": None}
    )
