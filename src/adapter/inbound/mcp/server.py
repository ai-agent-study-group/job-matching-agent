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
    from adapter.outbound.source.api.arbeitsagentur.client import ArbeitsagenturClient
    from service.job import JobService

    create_server(JobService(ArbeitsagenturClient())).run()
