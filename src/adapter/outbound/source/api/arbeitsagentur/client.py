"""연방고용청 API 호출."""

import asyncio
import base64
from typing import Any

import httpx2  # CRUD

from adapter.outbound.source.api.arbeitsagentur.dto import (
    ArbeitsagenturJobDTO,
    ArbeitsagenturSearchRequestDTO,
)
from domain.job import JobPosting
from port.outbound.source import JobSource

API = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}  # 공개 클라이언트 키 (https://jobsuche.api.bund.dev)
MAX_POSTINGS = 300


class ArbeitsagenturClient(JobSource):
    """연방고용청 공고 API 검색 어댑터."""

    async def usage(self) -> type[ArbeitsagenturSearchRequestDTO]:
        return ArbeitsagenturSearchRequestDTO

    async def search(self, params: dict[str, Any]) -> list[JobPosting]:
        """Validate params against the usage DTO and return matching postings."""
        p = ArbeitsagenturSearchRequestDTO.model_validate(params)
        # keywords · locations 말고는 그대로 API에 보냄. None을 보내면 400
        filters = {
            name: _to_query(value)
            for name, value in p.model_dump(
                exclude={"keywords", "locations"}, exclude_none=True
            ).items()
        }
        # API는 요청 하나에 키워드(was) 하나, 위치(wo) 하나만 받음
        # 요청이 하나라도 실패하면 전체를 실패시킴 (의도함).
        # 성공한 것만 주면 LLM이 빠진 조합(예: 틀린 지명)을 모름. 성공 · 실패를 같이 주려면
        # 반환 모양(list[JobPosting])을 포트 · 서비스 · 도구까지 바꿔야 해서 지금은 하지 않음.
        pairs = [(k, loc) for k in p.keywords for loc in p.locations or [None]]
        async with httpx2.AsyncClient(headers=HEADERS, timeout=30) as client:
            pages = await asyncio.gather(
                *(self._search(client, k, loc, filters) for k, loc in pairs)
            )
        found = _merge(pages)
        # 상한보다 많으면 보내지 않고 좁히라고 함
        if len(found) > MAX_POSTINGS:
            raise ValueError(
                f"More than {MAX_POSTINGS} postings match. Narrow the search, e.g. with "
                "veroeffentlichtseit, arbeitszeit, befristung, umkreis or more specific keywords."
            )
        return [job.to_summary() for job in found]

    async def fetch(self, posting_id: str) -> JobPosting:
        """Return one posting with its description."""
        # 상세 조회는 참조번호를 base64로 넣음
        ref = base64.b64encode(posting_id.encode()).decode()
        async with httpx2.AsyncClient(headers=HEADERS) as client:
            response = await client.get(f"{API}/pc/v4/jobdetails/{ref}")
        # 없는 참조번호는 404
        if response.status_code == 404:
            raise ValueError(
                f"No posting with id '{posting_id}'. Use an id from the search results."
            )
        response.raise_for_status()
        return ArbeitsagenturJobDTO.model_validate(response.json()).to_posting()

    async def _search(
        self,
        client: httpx2.AsyncClient,
        keyword: str,
        location: str | None,
        filters: dict[str, Any],
    ) -> list[ArbeitsagenturJobDTO]:
        # 디폴트는 상한 + 1 건으로 호출해보고, 검색 결과가 이것보다 많으면 범위를 좁히라고 함
        query = {"was": keyword, "size": MAX_POSTINGS + 1, **filters}
        if location:
            query["wo"] = location
        response = await client.get(f"{API}/pc/v6/jobs", params=query)
        response.raise_for_status()
        data = response.json()
        # 모르는 지명(예: Munich)은 오류 없이 0건으로 옴
        if data.get("woOutput", {}).get("suchmodus") == "UNGUELTIG":
            raise ValueError(
                f"Unknown location '{location}'. Use German place names, e.g. München."
            )
        # 결과가 없으면 "ergebnisliste" 키가 빠짐
        return [ArbeitsagenturJobDTO.model_validate(j) for j in data.get("ergebnisliste", [])]


def _to_query(value: Any) -> Any:
    # 목록은 ";"로 이어야 함 (같은 키를 반복하면 오류 없이 0건)
    return ";".join(map(str, value)) if isinstance(value, list) else value


def _merge(pages: list[list[ArbeitsagenturJobDTO]]) -> list[ArbeitsagenturJobDTO]:
    """조합별 검색 결과를 합쳐, 같은 공고(같은 참조번호)는 하나로 만든다.

    같은 공고가 여러 조합의 결과에 나올 수 있음:
    - 키워드가 여러 개면 키워드마다 나옴
    - 근무지가 여러 곳인 공고는 지명마다 나옴. 이때 검색 목록은 그 공고의 근무지 중 검색한
      지명과 맞는 곳 하나만 보여 줌 (예: 근무지 8곳인 공고가 München 검색에서는 München만,
      Berlin 검색에서는 Berlin만)

    그래서 처음 나온 공고를 남기고, 다시 나오면 근무지만 그 공고에 이어 붙임.
    예: München 검색의 [München] + Berlin 검색의 [Berlin] → [München, Berlin].
    같은 도시가 여러 번 들어가도 to_summary()가 한 번만 씀.
    """
    found: dict[str, ArbeitsagenturJobDTO] = {}
    for page in pages:
        for job in page:
            if job.referenznummer in found:
                found[job.referenznummer].stellenlokationen += job.stellenlokationen
            else:
                found[job.referenznummer] = job
    return list(found.values())
