import pytest
from pydantic_ai.models.test import TestModel

from src.adapter.inbound.agent.profile_agent import (
    create_profile_agent,
    extract_profile,
)
from src.domain.profile import SearchQuery


# 테스트 1: 이력서 텍스트를 입력하면 SearchQuery 객체가 반환되는지 확인
@pytest.mark.asyncio
async def test_extract_profile():
    agent = create_profile_agent()

    # 실제 OpenAI API를 호출하지 않고 TestModel 사용
    with agent.override(model=TestModel()):
        query = await extract_profile(
            "Data Analyst with Python and SQL experience.",
            agent=agent,
        )

    # 반환된 데이터가 SearchQuery 모델인지 확인
    assert isinstance(query, SearchQuery)
    assert isinstance(query.keywords, str)
    assert isinstance(query.location, str)


# 테스트 2: 빈 이력서가 입력되면 ValueError가 발생하는지 확인
@pytest.mark.asyncio
async def test_empty_resume():
    with pytest.raises(ValueError, match="Resume text cannot be empty"):
        await extract_profile("   ")


# 테스트 3: LLM 결과가 SearchQuery 필드에 정확히 매핑되는지 확인
@pytest.mark.asyncio
async def test_profile_field_mapping():
    agent = create_profile_agent()

    # 테스트에서 LLM이 반환할 가상의 검색 조건
    expected = {
        "keywords": "Data Analyst Python SQL Power BI",
        "location": "Berlin",
    }

    # TestModel을 이용해 지정된 결과를 반환하도록 설정
    with agent.override(model=TestModel(custom_output_args=expected)):
        query = await extract_profile(
            "Data Analyst with 3 years of experience. "
            "Skills: Python, SQL, Power BI. "
            "Preferred location: Berlin.",
            agent=agent,
        )

    # 반환 결과가 예상한 검색 조건과 일치하는지 확인
    assert query.model_dump() == expected


# 테스트 4: 희망 근무 지역이 없는 경우 빈 문자열을 허용하는지 확인
@pytest.mark.asyncio
async def test_missing_location():
    agent = create_profile_agent()

    expected = {
        "keywords": "Python SQL",
        "location": "",
    }

    with agent.override(model=TestModel(custom_output_args=expected)):
        query = await extract_profile(
            "Skills: Python, SQL.",
            agent=agent,
        )

    assert query.model_dump() == expected
