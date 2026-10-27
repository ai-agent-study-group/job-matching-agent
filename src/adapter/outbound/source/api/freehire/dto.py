"""freehire 검색 파라미터 · 응답 DTO와 도메인 변환."""

from datetime import datetime
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from adapter.outbound.source.api.freehire.text_parser import to_text
from domain.job import JobPosting

# 나라 · 언어 코드 (de, en). 대문자로 와도 소문자로 바꿈 (freehire는 소문자를 씀)
Code = Annotated[str, StringConstraints(min_length=2, max_length=2, to_lower=True)]


class FreehireSearchRequestDTO(BaseModel):
    """Search parameters for freehire (postings from company career pages, worldwide)."""

    # 모르는 키가 오면 오류 (Pydantic 기본값은 조용히 버림)
    model_config = ConfigDict(extra="forbid")

    q: str = Field(
        min_length=1,
        description="Job titles or skills, e.g. AI Engineer. "
        "Plain words: the first ones are required, later ones are dropped when few postings "
        "match, so AI Engineer can also return AI Product Manager. Quote words to require "
        'all of them, e.g. "AI Engineer" (any order and position, not an exact phrase). '
        "-word leaves out postings with that word, e.g. -junior. "
        'Join alternatives with OR (uppercase, at most 5), e.g. "AI Engineer" OR "ML Engineer"',
    )
    q_fields: list[Literal["title", "company", "description", "location"]] | None = Field(
        None,
        description="Fields q is matched in (default: all four). "
        'e.g. ["title"] leaves out postings that mention q only in the company name or body',
    )
    cities: list[Annotated[str, Field(min_length=1)]] = Field(
        [], description="City names, e.g. Berlin, München. Give cities or countries"
    )
    countries: list[Code] = Field(
        [],
        description="Lowercase ISO country codes, e.g. de. With cities, keeps only "
        "postings in these countries. Give cities or countries",
    )
    work_mode: list[Literal["remote", "hybrid", "onsite"]] | None = Field(
        None, description="Postings that state no work mode are left out"
    )
    seniority: (
        list[
            Literal["intern", "junior", "middle", "senior", "lead", "staff", "principal", "c_level"]
        ]
        | None
    ) = Field(None, description="Postings that state no seniority are left out")
    seniority_include_unspecified: bool | None = Field(
        None, description="true keeps postings that state no seniority when seniority is given"
    )
    employment_type: (
        list[Literal["full_time", "part_time", "contract", "internship", "fellowship"]] | None
    ) = Field(None, description="Postings that state no employment type are left out")
    posting_language: list[Code] | None = Field(
        None, description="Language the posting is written in, e.g. en, de"
    )
    visa_sponsorship: bool | None = Field(
        None, description="true keeps only postings that state visa sponsorship"
    )
    posted_within_days: int | None = Field(
        None, ge=1, le=36500, description="Only postings published in the last N days"
    )
    reality: list[Literal["fresh", "stale", "likely-evergreen"]] | None = Field(
        None,
        description="fresh: recent and not reposted, stale: old, "
        "likely-evergreen: always-open hiring ad",
    )

    @model_validator(mode="after")
    def _needs_place(self) -> Self:
        # 위치가 없으면 전 세계 공고를 찾아서 거의 항상 상한을 넘음
        if not self.cities and not self.countries:
            raise ValueError("Give at least one of cities or countries")
        return self


JOB_PAGE = "https://freehire.me/jobs"


class FreehireJobDTO(BaseModel):
    """One posting from a search result or the detail endpoint (full body only in the latter)."""

    public_slug: str  # 공고 id
    title: str  # 직무명
    company: str  # 회사
    location: str = ""  # 공고에 적힌 근무지 그대로
    description: str | None = None  # 본문 HTML (검색 결과에는 앞부분만)
    countries: list[str] = []  # 나라 코드. 도시 + 나라 검색에서 나라로 거를 때만 씀
    closed_at: datetime | None = None  # 마감 시각 (공고 하나 조회에서만 옴)

    def to_summary(self) -> JobPosting:
        """Same as to_posting(), but without url and description. For search results."""
        return JobPosting(
            source="freehire",
            id=self.public_slug,
            company=self.company,
            title=self.title,
            location=self.location,
        )

    def to_posting(self) -> JobPosting:
        """The full posting, with url and description. For a single fetched posting."""
        return self.to_summary().model_copy(
            update={
                # 약관상 보여 주는 공고마다 freehire 링크가 있어야 해서 회사 지원 페이지 대신 씀
                "url": f"{JOB_PAGE}/{self.public_slug}",
                "description": to_text(self.description) if self.description else None,
            }
        )
