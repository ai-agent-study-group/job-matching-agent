"""Search agent: find job postings using MCP tools."""

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.messages import ToolReturnPart

from domain.job import JobPosting

SEARCH_PROMPT = """
You are a job search agent.
The user message is a candidate Profile in JSON.
Your job is to find postings that match it.
The postings are collected from your search_jobs results,
and their full text is read in a later step.

1. Call list_sources and pick the source that fits the Profile.
2. Call get_usage(source) and build params from that schema
   using the Profile.
   Follow each field's description, e.g. the language of place names.
3. Call search_jobs(source, params) once.
   If it returns an error, fix params as the error says
   and call it again.
4. After the search, reply with one short line.
   Do not list the postings.
"""


def create_search_agent(
    model: str,
    mcp_toolset: MCPToolset,
) -> Agent:
    """Create a search agent connected to MCP tools."""
    return Agent(
        model,
        toolsets=[mcp_toolset.filtered(lambda ctx, tool: tool.name != "get_job")],
        instructions=SEARCH_PROMPT,
        output_type=str,
        retries={"tools": 5},
    )


def extract_jobs(result) -> list[JobPosting]:
    jobs = []
    seen = set()

    for message in result.all_messages():
        for part in message.parts:
            if not isinstance(part, ToolReturnPart):
                continue

            if part.tool_name != "search_jobs":
                continue

            if not isinstance(part.content, list):
                continue

            for item in part.content:
                job = JobPosting.model_validate(item)

                key = (job.source, job.id)

                if key in seen:
                    continue

                seen.add(key)
                jobs.append(job)

    return jobs
