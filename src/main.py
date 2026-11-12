"""조립: 어댑터를 service에 연결하고 /api와 /mcp를 한 FastAPI 앱에 올림."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic_ai.mcp import MCPToolset

from adapter.inbound.agent.job_summarizer import create_job_summarizer_agent
from adapter.inbound.agent.profile import create_profile_agent
from adapter.inbound.agent.search import create_search_agent
from adapter.inbound.api.route import router as api_router
from adapter.inbound.mcp.server import create_server
from adapter.outbound.source.api.arbeitsagentur.client import ArbeitsagenturClient
from service.job import JobService
from service.registry import RegistryService


@asynccontextmanager
async def lifespan(app: FastAPI):
    model = os.environ["LLM_MODEL"]

    async with ArbeitsagenturClient() as arbeitsagentur:
        registry = RegistryService([JobService(arbeitsagentur)])

        mcp_server = create_server(registry)
        mcp_toolset = MCPToolset(mcp_server)

        app.state.mcp_server = mcp_server
        app.state.job_summarizer_agent = create_job_summarizer_agent(model)
        # route.py에서 사용
        app.state.profile_agent = create_profile_agent(model)
        app.state.search_agent = create_search_agent(model, mcp_toolset)

        yield


app = FastAPI(
    title="job-matching-agent API",
    lifespan=lifespan,
)

app.include_router(api_router)
