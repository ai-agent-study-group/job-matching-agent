"""JobService: get_usage · search_jobs · get_job (JobServicePort 구현)."""

from typing import Annotated, Any

from pydantic import Field, ValidationError

from domain.job import JobPosting
from port.inbound.job import JobServicePort
from port.outbound.source import JobSource


class JobService(JobServicePort):
    def __init__(self, source: JobSource):
        self.source = source

    async def get_usage(self) -> dict[str, Any]:
        """Return the parameters search_jobs accepts, as a JSON schema.

        Call this before search_jobs.
        """
        return (await self.source.usage()).model_json_schema()

    async def search_jobs(
        self,
        params: Annotated[
            dict[str, Any], Field(description="Search parameters exactly as described by get_usage")
        ],
    ) -> list[JobPosting]:
        """Search job postings."""
        try:
            return await self.source.search(params)
        except ValidationError as e:
            # params를 지어내서 틀렸을 때, 사용법 도구를 먼저 부르도록 안내함
            raise ValueError(
                f"{e}\nCall get_usage first to see the params search_jobs accepts."
            ) from e

    async def get_job(
        self,
        posting_id: Annotated[
            str, Field(description="The id of a posting returned by search_jobs")
        ],
    ) -> JobPosting:
        """Return one posting with its full description."""
        return await self.source.fetch(posting_id)
