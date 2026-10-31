"""MCP 서버: JobServicePort의 함수를 도구로 등록."""

from fastmcp import FastMCP

from port.inbound.job import JobServicePort


def create_server(jobs: JobServicePort) -> FastMCP:
    mcp = FastMCP("jobs")
    for tool in (jobs.get_usage, jobs.search_jobs, jobs.get_job):
        mcp.tool(tool, annotations={"readOnlyHint": True})
    return mcp


if __name__ == "__main__":
    # 로컬에서 stdio로 실행할 때의 조립
    import asyncio

    from adapter.outbound.source.api.arbeitsagentur.client import ArbeitsagenturClient
    from adapter.outbound.source.api.freehire.client import FreehireClient
    from service.job import JobService

    # freehire는 약관상 개인 사용만 무료라 배포용 조립(src/main.py)에는 넣지 않음
    async def main() -> None:
        async with ArbeitsagenturClient() as arbeitsagentur, FreehireClient() as freehire:
            # 임시: JobService가 출처를 하나만 받아서 출처마다 서버를 만들어 합침. #9에서 바뀔 예정
            mcp = FastMCP("jobs")
            mcp.mount(create_server(JobService(arbeitsagentur)), namespace="arbeitsagentur")
            mcp.mount(create_server(JobService(freehire)), namespace="freehire")
            await mcp.run_async()

    asyncio.run(main())
