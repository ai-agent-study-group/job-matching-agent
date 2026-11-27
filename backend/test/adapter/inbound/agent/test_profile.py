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
            "seniority": "mid",
            "languages": [{"code": "de", "level": "fluent"}],
            "experiences": [
                {
                    "title": "Data Analyst",
                    "start": "2020-01",
                    "end": "2022-12",
                    "highlights": [{"text": "Built reports with SQL", "skills": ["SQL"]}],
                }
            ],
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
    assert result.output.seniority == "mid"
    assert result.output.experiences[0].highlights[0].skills == ["SQL"]
    # 계산 필드는 TestModel 출력에 없어도 경력에서 계산됨
    assert result.output.skills == ["SQL"]
    assert result.output.months_of_experience == 36
