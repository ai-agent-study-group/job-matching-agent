"""연방고용청 DTO: 응답을 도메인으로 바꾸는 것과 검색 파라미터 검사.

HTTP는 쓰지 않음. search_response.json은 실제 검색 응답을 공고 2건으로 줄인 것:
EXXETA(externeURL이 있는 제휴 업체 공고)와 BWI(externeURL이 없는 연방고용청 공고).
detail_response.json은 BWI 공고의 실제 상세 응답을 줄인 것 (본문은 앞부분만).
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from adapter.outbound.source.api.arbeitsagentur.dto import (
    JOB_PAGE,
    ArbeitsagenturJobDTO,
    ArbeitsagenturSearchRequestDTO,
)

SEARCH = json.loads((Path(__file__).parent / "search_response.json").read_text())
DETAIL = json.loads((Path(__file__).parent / "detail_response.json").read_text())


def test_to_posting_links_partner_postings_to_the_original():
    """제휴 업체 공고는 원래 공고로, 나머지는 연방고용청 공고 페이지로 연결한다.

    목적: 제휴 업체 공고의 연방고용청 페이지에는 280자 정도 요약만 있음.
    기대 결과: EXXETA의 url은 externeURL, BWI의 url은 JOB_PAGE/<참조번호>.
    """
    partner, own = (ArbeitsagenturJobDTO.model_validate(j) for j in SEARCH["ergebnisliste"])

    assert partner.to_posting().url == partner.externeURL
    assert own.to_posting().url == f"{JOB_PAGE}/{own.referenznummer}"


def test_to_posting_joins_each_city_once():
    """근무지 도시를 한 번씩만 잇고, 도시가 없는 주소는 건너뛴다.

    목적: 공고 하나에 같은 도시가 여러 번 나오거나 도시 없는 주소가 섞일 수 있음.
    기대 결과: München, München, Berlin, 빈 주소 → "München, Berlin".
    """
    job = ArbeitsagenturJobDTO(
        referenznummer="1",
        stellenangebotsTitel="AI Engineer",
        stellenlokationen=[
            {"adresse": {"ort": "München"}},
            {"adresse": {"ort": "München"}},
            {"adresse": {"ort": "Berlin"}},
            {"adresse": {}},
        ],
    )

    assert job.to_posting().location == "München, Berlin"


def test_search_request_rejects_unknown_keys():
    """DTO에 없는 키가 들어온 검색 파라미터는 거부한다.

    목적: Pydantic은 기본 설정에서 모르는 키를 조용히 버려서, LLM이 get_usage를 읽지 않고
    키를 지어내도(locations 대신 location) 그대로 통과함.
    기대 결과: ValidationError.
    """
    with pytest.raises(ValidationError):
        ArbeitsagenturSearchRequestDTO.model_validate(
            {"keywords": ["AI Engineer"], "location": "München"}
        )


def test_search_request_rejects_empty_text():
    """빈 키워드나 빈 지명이 든 검색 파라미터는 거부한다.

    목적: 빈 키워드("")는 API가 400으로 답하고, 빈 지명은 위치 없이 보내져서 그 조합만
    오류 없이 독일 전체를 검색함.
    기대 결과: keywords [""], locations ["München", ""] 모두 ValidationError.
    """
    with pytest.raises(ValidationError):
        ArbeitsagenturSearchRequestDTO.model_validate({"keywords": [""]})
    with pytest.raises(ValidationError):
        ArbeitsagenturSearchRequestDTO.model_validate(
            {"keywords": ["AI Engineer"], "locations": ["München", ""]}
        )


def test_to_summary_is_posting_without_url_and_description():
    """검색 결과용 변환(to_summary)은 to_posting에서 url과 본문만 뺀 것이다.

    목적: 검색 결과는 LLM에게 한 번에 최대 300건이 가서, url(공고 1건 토큰의 약 35%)과 본문을 빼고
    LLM이 고른 공고만 get_job(to_posting)으로 채움.
    기대 결과: 상세 응답 → to_posting은 url · description이 채워지고, to_summary는 그 둘만 None.
    """
    job = ArbeitsagenturJobDTO.model_validate(DETAIL)
    full, summary = job.to_posting(), job.to_summary()

    assert full.url == f"{JOB_PAGE}/{DETAIL['referenznummer']}"
    assert full.description == DETAIL["stellenangebotsBeschreibung"]
    assert summary == full.model_copy(update={"url": None, "description": None})
