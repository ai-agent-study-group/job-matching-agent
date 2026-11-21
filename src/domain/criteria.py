"""Qualifications (경력 수준 · 언어). 프로필과 공고가 같이 쓰는 값."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

Seniority = Literal["intern", "junior", "mid", "senior", "lead"]
LanguageLevel = Literal["basic", "good", "fluent", "native"]
# 앞뒤 공백을 떼고 빈 문자열을 막음. 예: "  SQL " → "SQL", "  " → 오류
NonBlank = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Language(BaseModel):
    code: NonBlank = Field(description='ISO 639-1 code, e.g. "de", "en".')
    level: LanguageLevel | None = Field(None, description="null if no level is stated.")


class Qualifications(BaseModel):
    seniority: Seniority | None = Field(None, description="Career level. null if unclear.")
    languages: list[Language] = Field(
        default_factory=list, description="Only languages explicitly stated."
    )
