"""MCP 서버: 출처 이름으로 RegistryService에서 JobService를 받아 부르는 도구 네 개."""

from typing import Annotated, Any

from fastmcp import FastMCP
from pydantic import Field

from domain.job import JobPosting
from domain.source import Source
from port.inbound.registry import RegistryServicePort

READ_ONLY = {"readOnlyHint": True}
SourceName = Annotated[str, Field(description="A source name returned by list_sources")]


def create_server(registry: RegistryServicePort) -> FastMCP:
    mcp = FastMCP("jobs")

    @mcp.tool(annotations=READ_ONLY)
    async def list_sources() -> list[Source]:
        """Return the job sources with a description of the postings each has.

        Call this first, pick the source that fits the request, and pass its name
        as source to the other tools.
        """
        return await registry.list_sources()

    @mcp.tool(annotations=READ_ONLY)
    async def get_usage(source: SourceName) -> dict[str, Any]:
        """Return the parameters search_jobs accepts for this source, as a JSON schema.

        Call this before search_jobs.
        """
        return await registry.get(source).get_usage()

    @mcp.tool(annotations=READ_ONLY)
    async def search_jobs(
        source: SourceName,
        params: Annotated[
            dict[str, Any], Field(description="Search parameters exactly as described by get_usage")
        ],
    ) -> list[JobPosting]:
        """Search job postings in one source."""
        return await registry.get(source).search_jobs(params)

    @mcp.tool(annotations=READ_ONLY)
    async def get_job(
        source: SourceName,
        posting_id: Annotated[
            str, Field(description="The id of a posting returned by search_jobs")
        ],
    ) -> JobPosting:
        """Return one posting with its full description."""
        return await registry.get(source).get_job(posting_id)

    return mcp


if __name__ == "__main__":
    # 로컬에서 stdio로 실행할 때의 조립
    import asyncio

    from adapter.outbound.source.api.arbeitsagentur.client import ArbeitsagenturClient
    from adapter.outbound.source.api.freehire.client import FreehireClient
    from service.job import JobService
    from service.registry import RegistryService

    # freehire는 약관상 개인 사용만 무료. src/main.py에는 시험용으로만 넣어 둠
    async def main() -> None:
        async with ArbeitsagenturClient() as arbeitsagentur, FreehireClient() as freehire:
            registry = RegistryService([JobService(arbeitsagentur), JobService(freehire)])
            await create_server(registry).run_async()

    asyncio.run(main())
