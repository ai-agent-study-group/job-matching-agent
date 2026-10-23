"""연방고용청 검색 파라미터 · 응답 DTO와 도메인 변환."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from domain.job import JobPosting


class ArbeitsagenturSearchRequestDTO(BaseModel):
    """Search parameters for the German Federal Employment Agency (all of Germany)."""

    # 모르는 키가 오면 오류 (Pydantic 기본값은 조용히 버림)
    model_config = ConfigDict(extra="forbid")

    # 빈 글자는 거부: 빈 키워드는 400, 빈 지명은 그 조합만 오류 없이 독일 전체를 검색함
    keywords: list[Annotated[str, Field(min_length=1)]] = Field(
        description="Job titles or skills, e.g. AI Engineer"
    )
    locations: list[Annotated[str, Field(min_length=1)]] = Field(
        [], description="German place names, e.g. München (not Munich). Empty means all of Germany"
    )
    umkreis: int | None = Field(None, description="Radius in km around each location (default 25)")
    berufsfeld: str | None = Field(None, description="Occupational field, e.g. Informatik")
    # 문서에 없는 파라미터 (beruf · arbeitsort · pav · externestellenboersen · quereinstieg).
    # 2026-10-21에 실제 API로 동작을 확인함. 예고 없이 바뀔 수 있음
    beruf: str | None = Field(
        None, description="Specific occupation, e.g. Anwendungsprogrammierer/in"
    )
    arbeitgeber: str | None = Field(None, description="Employer name, e.g. BMW AG")
    arbeitsort: str | None = Field(None, description="Exact town of the workplace, e.g. Gilching")
    angebotsart: Literal[1, 2, 4, 34] | None = Field(
        None,
        description="1 job, 2 self-employment, 4 vocational training or dual study, 34 internship",
    )
    arbeitszeit: list[Literal["vz", "tz", "snw", "mj"]] | None = Field(
        None, description="vz full-time, tz part-time, snw shifts/nights/weekends, mj mini job"
    )
    befristung: list[Literal[1, 2]] | None = Field(None, description="1 fixed-term, 2 permanent")
    veroeffentlichtseit: int | None = Field(
        None, ge=0, le=100, description="Only postings published in the last N days"
    )
    zeitarbeit: bool | None = Field(None, description="false excludes temporary agency postings")
    pav: bool | None = Field(None, description="false excludes private recruitment agencies")
    externestellenboersen: bool | None = Field(
        None, description="false excludes postings from external job boards (short summary only)"
    )
    quereinstieg: bool | None = Field(
        None, description="true keeps only postings open to career changers"
    )
    behinderung: bool | None = Field(
        None, description="true keeps only postings for people with disabilities"
    )


JOB_PAGE = "https://www.arbeitsagentur.de/jobsuche/jobdetail"


class ArbeitsagenturJobDTO(BaseModel):
    """One posting from a search result or the detail endpoint (body only in the latter)."""

    referenznummer: str  # 참조번호
    stellenangebotsTitel: str  # 직무명
    firma: str = ""  # 회사
    stellenlokationen: list[dict[str, Any]] = []  # 근무지: [{"adresse": {"ort": ...}}, ...]
    externeURL: str | None = None  # 제휴 업체 공고의 원래 링크
    stellenangebotsBeschreibung: str | None = None  # 본문

    def to_summary(self) -> JobPosting:
        """Same as to_posting(), but without url and description. For search results."""
        cities = [loc.get("adresse", {}).get("ort") for loc in self.stellenlokationen]
        return JobPosting(
            source="arbeitsagentur",
            id=self.referenznummer,
            company=self.firma,
            title=self.stellenangebotsTitel,
            location=", ".join(dict.fromkeys(city for city in cities if city)),
        )

    def to_posting(self) -> JobPosting:
        """The full posting, with url and description. For a single fetched posting."""
        return self.to_summary().model_copy(
            update={
                # 제휴 업체 공고는 연방고용청 페이지에 요약만 있어서 원래 링크를 우선함
                "url": self.externeURL or f"{JOB_PAGE}/{self.referenznummer}",
                "description": self.stellenangebotsBeschreibung,
            }
        )
