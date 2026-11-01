from pydantic import BaseModel, Field


class Profile(BaseModel):
    """이력서에서 추출한 지원자 정보를 구조화하여 저장하는 데이터 모델."""

    # 이력서에 명시된 직무 및 직책
    # 예: ["Data Analyst", "Operations Specialist"]
    job_titles: list[str] = Field(default_factory=list)

    # 지원자가 보유한 기술 및 업무 관련 역량
    # 예: ["Python", "SQL", "Power BI"]
    skills: list[str] = Field(default_factory=list)

    # 총 경력 연차 (소수점 허용)
    # 경력을 확인할 수 없으면 None
    # ge=0은 0 이상의 값만 허용한다는 의미
    years_of_experience: float | None = Field(default=None, ge=0)

    # 이력서에 명시된 사용 가능 언어
    # 예: ["Korean", "English", "German"]
    languages: list[str] = Field(default_factory=list)

    # 지원자가 명시적으로 희망하는 근무 지역
    # 예: ["Berlin", "Munich"]
    # 거주지만 기재된 경우 희망 지역으로 간주하지 않음
    preferred_locations: list[str] = Field(default_factory=list)
