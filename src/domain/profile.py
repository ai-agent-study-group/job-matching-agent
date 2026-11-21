"""Profile (이력서에서 뽑은 경력 · 학력 · 기술)."""

import re
from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from domain.criteria import NonBlank, Qualifications

# 응답에만 있는 계산 필드 이름
COMPUTED = ("skills", "months_of_experience")


class Highlight(BaseModel):
    text: NonBlank = Field(
        description=(
            "One bullet or line of a role, copied as written, including tech stack lines. "
            "Do not summarize or split."
        )
    )
    skills: list[NonBlank] = Field(
        default_factory=list,
        description=(
            "Tools, technologies and certificates named in this sentence, "
            "in their common official name."
        ),
    )


class Experience(BaseModel):
    title: NonBlank
    company: str | None = None
    start: str | None = Field(None, description='"YYYY-MM" or "YYYY".')
    end: str | None = Field(None, description='"YYYY-MM" or "YYYY". null if current.')
    highlights: list[Highlight] = Field(default_factory=list)


class Education(BaseModel):
    degree: NonBlank = Field(
        description='Degree or vocational training as written, e.g. "M.Sc.", "Ausbildung".'
    )
    subject: str | None = None
    end: str | None = Field(None, description='"YYYY-MM" or "YYYY". null if ongoing.')


def _month(value: str | None, default_month: int) -> int | None:
    """Return the month count since year 0 for "YYYY-MM" or "YYYY", else None."""
    match = re.fullmatch(r"(\d{4})(?:-(\d{1,2}))?", value or "")
    if not match:
        return None
    year, month = int(match[1]), int(match[2] or default_month)
    # 있을 수 없는 날짜는 읽지 않음. 예: "0000", "1899-05", "2020-13"
    if year < 1900 or not 1 <= month <= 12:
        return None
    return year * 12 + month


class Profile(Qualifications):
    # 응답 스키마에서 기본값 있는 필드도 필수로 적음 (FE TS 타입에 `?`가 안 붙게)
    # 모르는 키는 오류로 막음 (예: `experience` 오타, 예전 `{"resume_text": ...}` 형식)
    model_config = ConfigDict(json_schema_serialization_defaults_required=True, extra="forbid")

    experiences: list[Experience] = Field(default_factory=list)
    educations: list[Education] = Field(default_factory=list)
    other_skills: list[NonBlank] = Field(
        default_factory=list,
        description="Skills listed outside any role, e.g. a Skills section.",
    )

    @model_validator(mode="before")
    @classmethod
    def drop_computed(cls, data: Any) -> Any:
        # 계산 필드는 받지 않고 새로 계산. 예: FE가 /api/profile 응답을 그대로 다시 보낸 경우
        if isinstance(data, dict):
            return {key: value for key, value in data.items() if key not in COMPUTED}
        return data

    @computed_field
    @property
    def skills(self) -> list[str]:
        # 같은 기술은 처음 나온 하나만 남김. 예: ["SQL", "Python", "SQL"] → ["SQL", "Python"]
        found = [s for e in self.experiences for h in e.highlights for s in h.skills]
        return list(dict.fromkeys(found + self.other_skills))

    @computed_field
    @property
    def months_of_experience(self) -> int:
        # 겹치는 기간은 한 번만 셈. 예: 2020-01~2020-12와 2020-07~2021-06 → 18개월
        # 연도만 있으면 시작은 1월, 끝은 12월. end가 없으면(재직 중) 오늘까지
        today = date.today().year * 12 + date.today().month
        months: set[int] = set()
        for experience in self.experiences:
            start = _month(experience.start, 1)
            end = today if experience.end is None else _month(experience.end, 12)
            # 날짜를 읽을 수 없는 경력은 세지 않음. 예: start가 없거나 "2021 봄"
            if start is not None and end is not None:
                # 아직 오지 않은 달은 세지 않음. 예: 2027-06까지 계약이어도 오늘까지만
                months.update(range(start, min(end, today) + 1))
        return len(months)
