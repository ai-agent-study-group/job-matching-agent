"""JobPosting (공고 원문)"""

from pydantic import BaseModel, ConfigDict, Field


class JobPosting(BaseModel):
    """A job posting from a source, converted to our common format."""

    # 응답 스키마에서 기본값 있는 필드도 필수로 적음 (FE TS 타입에 `?`가 안 붙게)
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)

    source: str = Field(description="Source of the posting, e.g. arbeitsagentur")
    id: str = Field(description="Posting id within the source")
    company: str = Field(description="Company name")
    title: str = Field(description="Job title")
    location: str = Field(description="Location as written by the source")
    url: str | None = Field(
        default=None, description="Posting page URL; only set when a single posting is fetched"
    )
    description: str | None = Field(
        default=None,
        description="Posting body as plain text; only set when a single posting is fetched",
    )
