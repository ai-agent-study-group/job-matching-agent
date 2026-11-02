from pydantic_ai import Agent

from src.domain.profile import Profile

# LLM에게 전달할 시스템 지시문
# 이력서의 실제 경력과 기술을 바탕으로 적합한 직무명을 추출
# 희망 근무지는 명시적으로 적힌 경우에만 추출
INSTRUCTIONS = """
You are an AI agent that extracts job profile information from resume text.

Extract the following fields:

1. job_titles:
   - Identify job titles that match the candidate's actual experience
     and technical skills.
   - Use titles commonly found in job postings.
   - Job titles may be inferred from demonstrated skills and experience,
     even if they are not explicitly mentioned in the resume.
   - Use English or German job titles as appropriate.
   - Include German job titles when relevant to jobs in Germany.
   - Do not invent experience, qualifications, or skills.

2. locations:
   - Extract only preferred work locations explicitly stated in the resume.
   - Do not assume that the candidate's current address is a preferred
     work location.
   - Return an empty list if no preferred work location is specified.

Return the result according to the Profile schema.
"""


def create_profile_agent(model: str) -> Agent[None, Profile]:
    """Create a profile extraction agent with the specified LLM model."""

    # 전달받은 모델 이름으로 Agent 생성
    # LLM의 출력은 Profile 스키마에 따라 검증됨
    return Agent(
        model,
        output_type=Profile,
        instructions=INSTRUCTIONS,
    )
