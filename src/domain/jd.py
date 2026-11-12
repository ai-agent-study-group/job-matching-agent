"""JD: structured job requirements extracted from a posting."""

from typing import Literal

from pydantic import BaseModel, Field


class JD(BaseModel):
    """Structured job description for matching."""

    source: str
    posting_id: str

    title: str
    company: str
    location: str | None = None

    # Job responsibilities
    responsibilities: list[str] = Field(default_factory=list)

    # Technical skills and domain-specific competencies
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)

    # Soft skills
    required_soft_skills: list[str] = Field(default_factory=list)
    preferred_soft_skills: list[str] = Field(default_factory=list)

    # Education and other qualifications
    required_qualifications: list[str] = Field(default_factory=list)
    preferred_qualifications: list[str] = Field(default_factory=list)

    # Experience
    min_years_experience: int | None = Field(default=None, ge=0)

    # Language requirements
    required_languages: list[str] = Field(default_factory=list)
    preferred_languages: list[str] = Field(default_factory=list)

    # Work arrangement
    work_mode: Literal["remote", "hybrid", "onsite"] | None = None
