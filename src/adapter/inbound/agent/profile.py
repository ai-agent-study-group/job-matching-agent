import os

from dotenv import load_dotenv
from pydantic_ai import Agent

from src.domain.profile import SearchQuery

# 프로젝트 루트의 .env 파일에서 환경변수를 불러옴
# 예: OPENAI_API_KEY, PROFILE_AGENT_MODEL
load_dotenv()


# LLM에게 전달할 시스템 지시문
# 이력서 텍스트에서 필요한 정보를 추출하고
# Profile 모델의 필드에 맞게 구조화하도록 지시
INSTRUCTIONS = """
당신은 이력서 텍스트에서 지원자의 정보를 추출하는 에이전트입니다.

다음 항목을 추출하세요.
- keywords: 이력서에 명시된 직무와 기술을 바탕으로
  채용공고 검색에 사용할 핵심 키워드
- location: 이력서에 명시적으로 나타난 희망 근무 지역

규칙:
- 이력서에 없는 직무나 기술을 임의로 생성하지 마세요.
- 현재 거주지를 희망 근무 지역으로 간주하지 마세요.
- 희망 근무 지역이 없으면 빈 문자열("")을 반환하세요.
- 키워드를 추출할 수 없으면 빈 문자열("")을 반환하세요.
- 반드시 SearchQuery 스키마에 맞는 결과를 반환하세요.
"""


def create_profile_agent(model: str | None = None) -> Agent:
    """
    이력서 분석에 사용할 Profile Agent를 생성하는 함수.

    Args:
        model: 사용할 LLM 모델명.
               지정하지 않으면 .env의 PROFILE_AGENT_MODEL을 사용하고,
               해당 환경변수도 없으면 openai:gpt-4.1-mini를 사용함.

    Returns:
        Profile 형식으로 결과를 반환하도록 설정된 Agent 객체.
    """

    # 함수 인자로 전달된 모델을 우선 사용
    # 없으면 환경변수, 그것도 없으면 기본 모델 사용
    model_name = model or os.getenv("PROFILE_AGENT_MODEL", "openai:gpt-4.1-mini")

    return Agent(
        model_name,
        output_type=SearchQuery,  # LLM 출력을 Profile 모델로 검증
        instructions=INSTRUCTIONS,  # LLM이 따라야 할 정보 추출 규칙
    )


async def extract_profile(
    resume_text: str,
    agent: Agent | None = None,
) -> SearchQuery:
    """
    이력서 텍스트를 분석하여 Profile 객체로 변환하는 함수.

    Args:
        resume_text: 분석할 이력서 텍스트.
        agent: 사용할 Agent 객체.
               전달하지 않으면 기본 Profile Agent를 생성함.
               테스트 시 Mock Agent를 주입할 수 있음.

    Returns:
        이력서에서 추출한 정보를 담은 Profile 객체.

    Raises:
        ValueError: 이력서 텍스트가 비어 있는 경우.
    """

    # 공백만 있거나 빈 문자열이면 LLM을 호출하지 않고 오류 발생
    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    # 전달받은 Agent가 있으면 사용하고, 없으면 새로 생성
    profile_agent = agent or create_profile_agent()

    # LLM에 이력서 텍스트를 전달하여 분석 실행
    # await는 비동기 LLM 호출이 완료될 때까지 기다림
    result = await profile_agent.run(resume_text)

    # LLM 결과를 Profile 모델로 검증한 후 반환
    return SearchQuery.model_validate(result.output)
