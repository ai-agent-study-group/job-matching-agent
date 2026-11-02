import asyncio

from pydantic_ai.models.test import TestModel

from adapter.inbound.agent.profile import create_profile_agent
from domain.profile import Profile


def test_profile_agent_returns_profile():
    # 실제 API 호출 없이 테스트용 Agent 생성
    agent = create_profile_agent("test")

    # TestModel이 반환할 Profile 데이터 지정
    test_model = TestModel(
        custom_output_args={
            "job_titles": ["Data Analyst", "BI Analyst"],
            "locations": ["Berlin"],
        }
    )

    # 실제 LLM 대신 TestModel로 Agent 실행
    with agent.override(model=test_model):
        result = asyncio.run(
            agent.run(
                "I have experience with Python, SQL and Power BI. I am looking for a job in Berlin."
            )
        )

    # 결과가 Profile 객체인지 확인
    assert isinstance(result.output, Profile)
    assert result.output.job_titles == ["Data Analyst", "BI Analyst"]
    assert result.output.locations == ["Berlin"]
