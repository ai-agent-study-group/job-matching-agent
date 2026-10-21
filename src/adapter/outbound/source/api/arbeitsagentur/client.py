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


class ArbeitsagenturClient(JobSource):
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
        pairs = [(k, loc) for k in p.keywords for loc in p.locations or [None]]
        async with httpx2.AsyncClient(headers=HEADERS) as client:
            pages = await asyncio.gather(
                *(self._search(client, k, loc, filters) for k, loc in pairs)
            )
        # 같은 공고가 여러 조합에서 나오므로 참조번호로 하나만 남김
        found = {job.referenznummer: job for page in pages for job in page}
        return [job.to_posting() for job in found.values()]

    async def fetch(self, posting_id: str) -> JobPosting:
        """Return one posting with its description."""
        # 상세 조회는 참조번호를 base64로 넣음
        ref = base64.b64encode(posting_id.encode()).decode()
        async with httpx2.AsyncClient(headers=HEADERS) as client:
            response = await client.get(f"{API}/pc/v4/jobdetails/{ref}")
        response.raise_for_status()
        return ArbeitsagenturJobDTO.model_validate(response.json()).to_posting()

    async def _search(
        self,
        client: httpx2.AsyncClient,
        keyword: str,
        location: str | None,
        filters: dict[str, Any],
    ) -> list[ArbeitsagenturJobDTO]:
        query = {"was": keyword, **filters} | ({"wo": location} if location else {})
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
