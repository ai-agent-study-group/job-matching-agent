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


def test_to_posting_fills_description_only_from_detail():
    """상세 응답을 바꾸면 본문(description)이 채워지고, 검색 결과는 본문이 비어 있다.

    목적: 본문은 상세 응답의 stellenangebotsBeschreibung에만 있고 검색 결과에는 없음.
    기대 결과: 상세 응답 → description이 그 본문과 같음. 같은 공고의 검색 결과 → description은 None.
    """
    detail = ArbeitsagenturJobDTO.model_validate(DETAIL).to_posting()
    listed = ArbeitsagenturJobDTO.model_validate(SEARCH["ergebnisliste"][1]).to_posting()

    assert detail.id == listed.id == DETAIL["referenznummer"]
    assert detail.description == DETAIL["stellenangebotsBeschreibung"]
    assert listed.description is None
