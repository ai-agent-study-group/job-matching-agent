"""freehire 공고 API 호출."""

from typing import Any
from urllib.parse import quote

import httpx2  # CRUD

from adapter.outbound.source.api.freehire.dto import FreehireJobDTO, FreehireSearchRequestDTO
from domain.job import JobPosting
from port.outbound.source import JobSource

API = "https://freehire.me/api/v1"
HEADERS = {"User-Agent": "ai-agent-study-group/job-matching-agent"}  # freehire가 요청함
# API가 한 번에 주는 최대 건수. 상한을 더 올리려면 offset으로 나눠 받아야 함
MAX_POSTINGS = 100
# 쉬는 연결을 이 시간(초)이 지나면 버림. freehire(Cloudflare)가 400초 쉰 연결을 끊어서 여유를 둠
KEEPALIVE_SECONDS = 300


class FreehireClient(JobSource):
    """freehire 공고 API 검색 어댑터."""

    def __init__(self):
        # 서버가 떠 있는 동안 모든 요청이 이 클라이언트 하나를 같이 씀. 만들 때가 아니라 첫 요청 때 연결을 맺음.
        # 동시 연결은 10개까지, 쉬는 연결은 2개까지 보관. 넘치는 요청은 연결이 빌 때까지 기다림.
        # Limits를 넘기면 안 적은 값이 "제한 없음"이 돼서 셋 다 적음
        # 닫지 않음: 서버 프로세스와 수명이 같아서 끝날 때 운영체제가 닫음.
        # 서버가 도는 중에 어댑터를 새로 만들게 되면 닫는 코드(lifespan) 필요
        self.http = httpx2.AsyncClient(
            headers=HEADERS,
            timeout=30,
            limits=httpx2.Limits(
                max_connections=10,
                max_keepalive_connections=2,
                keepalive_expiry=KEEPALIVE_SECONDS,
            ),
        )

    async def usage(self) -> type[FreehireSearchRequestDTO]:
        return FreehireSearchRequestDTO

    async def search(self, params: dict[str, Any]) -> list[JobPosting]:
        """Validate params against the usage DTO and return matching postings."""
        request = FreehireSearchRequestDTO.model_validate(params)
        jobs = await self._search(_to_query(request))
        # 도시와 나라를 같이 받았으면 도시로 찾은 공고 중 그 나라 공고만 남김 (_to_query 참고)
        if request.cities and request.countries:
            jobs = [j for j in jobs if set(request.countries) & set(j.countries)]
        return [job.to_summary() for job in jobs]

    async def fetch(self, posting_id: str) -> JobPosting:
        """Return one posting with its description."""
        # id에 "/"가 있으면 다른 주소로 가므로 그대로 넣지 않음
        response = await self.http.get(f"{API}/jobs/{quote(posting_id, safe='')}")
        # 없는 공고 id는 404
        if response.status_code == 404:
            raise ValueError(
                f"No posting with id '{posting_id}'. Use an id from the search results."
            )
        response.raise_for_status()
        job = FreehireJobDTO.model_validate(response.json()["data"])
        # 공고 하나 조회는 마감된 공고도 돌려줌
        if job.closed_at:
            raise ValueError(f"Posting '{posting_id}' is closed.")
        return job.to_posting()

    async def _search(self, query: dict[str, Any]) -> list[FreehireJobDTO]:
        response = await self.http.get(f"{API}/jobs/search", params=query | {"limit": MAX_POSTINGS})
        # 잘못된 검색(OR 6개 이상 등)은 400과 이유가 옴
        if response.status_code == 400:
            raise ValueError(response.json()["error"])
        response.raise_for_status()
        body = response.json()
        meta = body["meta"]
        # 모르는 파라미터는 버리고, 허용 목록 밖 값은 0건으로 오류 없이 답함
        ignored = {key: meta[key] for key in ("ignored_params", "ignored_values") if key in meta}
        if ignored:
            raise ValueError(f"freehire did not apply part of the search: {ignored}")
        # 상한보다 많으면 보내지 않고 좁히라고 함
        if meta["total"] > MAX_POSTINGS:
            raise ValueError(
                f"More than {MAX_POSTINGS} postings match. Narrow the search, e.g. with "
                "cities, work_mode, seniority, posted_within_days or more specific keywords."
            )
        return [FreehireJobDTO.model_validate(j) for j in body["data"]]


def _to_query(request: FreehireSearchRequestDTO) -> dict[str, Any]:
    # list 일 경우 httpx가 같은 키를 반복해서 보냄 ("cities":["Berlin", "München"] -> cities=Berlin&cities=München).
    query = request.model_dump(exclude_none=True)
    # q_fields만 쉼표로 이은 글자 하나를 받음
    if request.q_fields:
        query["q_fields"] = ",".join(request.q_fields)
    # API는 위치를 OR로 묶어서 독일 + 베를린이면 독일 전체가 나옴.
    # 도시가 있으면 나라는 빼고 도시로만 찾음. 나라는 받은 공고에서 거름 (search 참고)
    if request.cities:
        del query["countries"]
    return query
