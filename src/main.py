"""조립: 어댑터를 service에 연결하고 /api와 /mcp를 한 FastAPI 앱에 올림."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic_ai.mcp import MCPToolset

from adapter.inbound.agent.profile import create_profile_agent
from adapter.inbound.agent.search import create_search_agent
from adapter.inbound.api.route import router as api_router
from adapter.inbound.mcp.server import create_server
from adapter.outbound.source.api.arbeitsagentur.client import ArbeitsagenturClient
from adapter.outbound.source.api.freehire.client import FreehireClient
from service.job import JobService
from service.registry import RegistryService

# 클라이언트는 여기서 만들기만 하고, HTTP 연결은 lifespan에서 열고 닫음
arbeitsagentur = ArbeitsagenturClient()
# 잠깐 시험용으로 넣음. freehire는 약관상 개인·비상업적 사용만 무료라 공개 배포 전에 뺄 것
freehire = FreehireClient()
registry = RegistryService([JobService(arbeitsagentur), JobService(freehire)])
mcp_server = create_server(registry)
mcp_app = mcp_server.http_app(path="/mcp")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    model = os.environ["LLM_MODEL"]
    # route.py에서 사용. 검색 agent는 /mcp와 같은 MCP 서버의 도구를 씀
    app.state.profile_agent = create_profile_agent(model)
    app.state.search_agent = create_search_agent(model, MCPToolset(mcp_server))
    # 앱이 떠 있는 동안 출처 HTTP 연결과 MCP 세션 관리자를 열어 둠
    async with arbeitsagentur, freehire, mcp_app.lifespan(app):
        yield


app = FastAPI(title="job-matching-agent API", lifespan=lifespan)
app.include_router(api_router)
# "/"에 붙여서 주소가 /mcp가 됨. 모든 경로를 받으므로 라우트는 이 줄보다 위에서 등록할 것
app.mount("/", mcp_app)
