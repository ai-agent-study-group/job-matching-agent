from pydantic import BaseModel, ConfigDict, Field


class Profile(BaseModel):
    """Profile information extracted from a candidate's resume."""

    # 응답 스키마에서 기본값 있는 필드도 필수로 적음 (FE TS 타입에 `?`가 안 붙게)
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)

    # 이력서의 경력과 기술에 맞는 직무명
    job_titles: list[str] = Field(
        default_factory=list,
        description=(
            "Relevant job titles based on the candidate's experience "
            "and skills. Use titles commonly found in job postings."
        ),
    )

    # 이력서에 명시된 희망 근무지 (없으면 빈 리스트)
    locations: list[str] = Field(
        default_factory=list,
        description=(
            "Preferred work locations explicitly stated in the resume. "
            "Do not infer preferences from the current address. "
            "Return an empty list if unspecified."
        ),
    )
