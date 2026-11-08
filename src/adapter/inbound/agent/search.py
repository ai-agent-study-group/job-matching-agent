"""Search agent: find job postings using MCP tools."""

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.messages import ToolReturnPart

from domain.job import JobPosting
from domain.profile import Profile

SEARCH_PROMPT = """
You are a job search agent.

Search for real job postings based on the candidate's Profile.

Follow these steps:
1. Call list_sources to discover available sources.
2. Select "arbeitsagentur".
3. Call get_usage("arbeitsagentur") to inspect the parameter schema.
4. Build search parameters using the Profile:
   - job_titles -> keywords
   - locations -> locations
5. Call search_jobs("arbeitsagentur", params).
6. Do not invent or modify job postings.
7. Do not call get_job.
8. Finish after receiving the search results.
"""


def create_search_agent(
    model: str,
    mcp_toolset: MCPToolset,
) -> Agent:
    """Create a search agent connected to MCP tools."""
    return Agent(
        model,
        toolsets=[mcp_toolset],
        instructions=SEARCH_PROMPT,
        output_type=str,
    )


async def run_search_agent(
    agent: Agent,
    profile: Profile,
) -> list[JobPosting]:
    result = await agent.run(profile.model_dump_json())
    return extract_jobs(result)


def extract_jobs(result) -> list[JobPosting]:
    """Extract original search_jobs results from agent messages."""
    jobs: list[JobPosting] = []

    for message in result.all_messages():
        for part in message.parts:
            if not isinstance(part, ToolReturnPart):
                continue

            if part.tool_name != "search_jobs":
                continue

            content = part.content

            if not isinstance(content, list):
                continue

            for item in content:
                jobs.append(JobPosting.model_validate(item))

    return jobs
