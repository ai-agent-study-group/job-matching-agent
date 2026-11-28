"""시작점: /api와 /mcp를 한 FastAPI 앱에 올림."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastmcp.server.auth import AuthProvider, TokenVerifier
from pydantic_ai.mcp import MCPToolset

from adapter.inbound.agent.profile import create_profile_agent
from adapter.inbound.agent.search import create_search_agent
from adapter.inbound.api.route import router as api_router
from adapter.inbound.auth import create_api_auth, create_mcp_auth
from adapter.inbound.mcp.server import create_server
from bootstrap import bootstrap
from observability import configure_logfire, instrument_fastapi


def create_app(
    mcp_auth: AuthProvider | None = None,
    api_auth: TokenVerifier | None = None,
) -> FastAPI:
    """/api와 /mcp를 묶은 FastAPI 앱을 만든다. 테스트에서는 환경 변수를 읽지 않게 이 함수를 직접 씀."""
    container = bootstrap()
    mcp_server = create_server(container.registry, auth=mcp_auth)
    mcp_app = mcp_server.http_app(path="/mcp")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        model = os.environ["LLM_MODEL"]
        # route.py에서 사용. 검색 agent는 /mcp와 같은 MCP 서버의 도구를 씀
        app.state.profile_agent = create_profile_agent(model)
        app.state.search_agent = create_search_agent(model, MCPToolset(mcp_server))
        # 앱이 떠 있는 동안 출처 연결과 MCP 세션 관리자를 열어 둠
        async with container.open(), mcp_app.lifespan(app):
            yield

    app = FastAPI(title="job-matching-agent API", lifespan=lifespan)
    app.state.api_auth = api_auth
    app.include_router(api_router)
    # "/"에 붙여서 주소가 /mcp가 됨. 모든 경로를 받으므로 라우트는 이 줄보다 위에서 등록할 것
    app.mount("/", mcp_app)
    return app


def create_prod_app() -> FastAPI:
    """서버 실행용 팩토리 (uvicorn --factory). 인증 설정과 Logfire를 연결한다."""
    # FastMCP 4가 만드는 MCP/OpenTelemetry span도 같은 Logfire 설정으로 내보낸다.
    configure_logfire()
    app = create_app(mcp_auth=create_mcp_auth(), api_auth=create_api_auth())
    instrument_fastapi(app)
    return app
