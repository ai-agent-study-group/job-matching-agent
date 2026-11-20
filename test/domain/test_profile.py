"""Profile 도메인: 계산 필드(skills, months_of_experience)와 입력 검사."""

from datetime import date

import pytest
from pydantic import ValidationError

from domain.profile import Profile


def experience(start, end, *skills):
    """기술 하나마다 문장 하나를 가진 경력."""
    highlights = [{"text": f"Used {skill}", "skills": [skill]} for skill in skills]
    return {"title": "Engineer", "start": start, "end": end, "highlights": highlights}


def test_skills_merges_highlights_and_other_skills_without_duplicates():
    profile = Profile(
        experiences=[
            experience("2021-01", "2021-12", "SQL", "Python"),
            experience("2020-01", "2020-12", "SQL", "Tableau"),
        ],
        other_skills=["Docker", "Python"],
    )

    assert profile.skills == ["SQL", "Python", "Tableau", "Docker"]


@pytest.mark.parametrize(
    ("periods", "months"),
    [
        # 한 경력: 시작 달과 끝 달을 모두 셈
        ([("2020-01", "2022-12")], 36),
        # 겹치는 기간은 한 번만 셈
        ([("2020-01", "2020-12"), ("2020-07", "2021-06")], 18),
        # 떨어진 경력은 더함
        ([("2019-01", "2019-06"), ("2021-01", "2021-06")], 12),
        # 연도만 있으면 시작은 1월, 끝은 12월
        ([("2020", "2021")], 24),
        # 날짜를 읽을 수 없는 경력은 세지 않음
        ([(None, "2021-12"), ("2021 spring", "2021-12"), ("2020-01", "2020-03")], 3),
    ],
)
def test_months_of_experience(periods, months):
    profile = Profile(experiences=[experience(start, end) for start, end in periods])

    assert profile.months_of_experience == months


def test_months_of_experience_counts_a_current_role_until_today():
    today = date.today()
    start = f"{today.year - 1}-{today.month:02d}"

    profile = Profile(experiences=[experience(start, None)])

    # 작년 이번 달부터 이번 달까지: 13개월
    assert profile.months_of_experience == 13


def test_computed_fields_are_not_in_the_llm_output_schema():
    """계산 필드는 LLM이 채우지 않는다.

    목적: 프로필 agent의 출력 스키마(검증용 스키마)에 계산 필드가 들어가면 LLM이 값을 지어냄.
    """
    properties = Profile.model_json_schema(mode="validation")["properties"]

    assert "skills" not in properties
    assert "months_of_experience" not in properties
    assert "experiences" in properties


def test_response_can_be_sent_back_as_input():
    """응답을 그대로 다시 넣어도 통과하고, 계산 필드는 새로 계산된다.

    목적: FE가 /api/profile 응답을 /api/search에 그대로 보냄. 계산 필드 키 때문에 422가 나면 안 됨.
    """
    profile = Profile(experiences=[experience("2020-01", "2020-12", "SQL")])
    sent_back = profile.model_dump() | {"skills": ["Fake"], "months_of_experience": 999}

    again = Profile.model_validate(sent_back)

    assert again.skills == ["SQL"]
    assert again.months_of_experience == 12


def test_unknown_key_is_rejected():
    with pytest.raises(ValidationError):
        Profile.model_validate({"job_titles": ["Data Analyst"]})
