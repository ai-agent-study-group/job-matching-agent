import asyncio

from pydantic_ai.models.test import TestModel

from src.adapter.inbound.agent.profile import create_profile_agent
from src.domain.profile import Profile


def test_profile_agent_returns_profile():
    # 실제 API 키 없이 테스트용 Agent 생성
    agent = create_profile_agent("test")

    # 실제 LLM 대신 TestModel 사용
    with agent.override(model=TestModel()):
        result = asyncio.run(
            agent.run(
                "I have experience with Python, SQL, and Power BI. "
                "I am looking for a job in Berlin."
            )
        )

    # 반환 결과가 Profile 객체인지 확인
    assert isinstance(result.output, Profile)

    # 두 필드가 문자열 리스트인지 확인
    assert isinstance(result.output.job_titles, list)
    assert isinstance(result.output.locations, list)


def test_profile_agent_returns_expected_fields():
    # 테스트에서 반환할 값을 미리 지정
    agent = create_profile_agent("test")

    test_model = TestModel(
        custom_output_args={
            "job_titles": ["Data Analyst", "BI Analyst"],
            "locations": ["Berlin"],
        }
    )

    with agent.override(model=test_model):
        result = asyncio.run(agent.run("Resume text"))

    # 반환 결과가 Profile 스키마와 일치하는지 확인
    assert result.output == Profile(
        job_titles=["Data Analyst", "BI Analyst"],
        locations=["Berlin"],
    )
