"""JobService: get_usage · search_jobs · get_job (JobServicePort 구현)."""

from typing import Any

from pydantic import ValidationError

from domain.job import JobPosting
from port.inbound.job import JobServicePort
from port.outbound.source import JobSource


class JobService(JobServicePort):
    """출처(JobSource) 하나를 받아 JobServicePort의 기능을 구현."""

    def __init__(self, source: JobSource):
        self.source = source

    def get_name(self) -> str:
        return self.source.name()

    def get_description(self) -> str:
        return self.source.description()

    async def get_usage(self) -> dict[str, Any]:
        return (await self.source.usage()).model_json_schema()

    async def search_jobs(self, params: dict[str, Any]) -> list[JobPosting]:
        try:
            return await self.source.search(params)
        except ValidationError as e:
            # params를 지어내서 틀렸을 때, 사용법 도구를 먼저 부르도록 안내함
            raise ValueError(
                f"{e}\nCall get_usage first to see the params search_jobs accepts."
            ) from e

    async def get_job(self, posting_id: str) -> JobPosting:
        return await self.source.fetch(posting_id)
