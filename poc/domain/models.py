"""PoC용 임시 스키마. 실제 계약은 src/schemas에서 팀 합의로 정함."""

from pydantic import BaseModel, Field


class JobSearch(BaseModel):
    board: str = Field(description="Greenhouse board token")
    role: str = Field(description="찾을 직무")
    limit: int = Field(default=3, description="구조화할 공고 수 상한")


class JobPosting(BaseModel):
    id: int
    title: str
    location: str
    required: list[str] = Field(description="필수 요건")
    preferred: list[str] = Field(description="우대 요건")
    stack: list[str] = Field(description="기술 스택")
    languages: list[str] = Field(description="업무 언어 요건 (예: English, German)")
    min_years: int | None = Field(description="최소 경력 연수. 명시 없으면 null")
