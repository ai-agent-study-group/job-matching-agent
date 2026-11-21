"""Logfire 설정과 앱 계측.

이력서 원문은 개인정보이므로 FastAPI 요청 인자와 Pydantic AI 메시지에
남기지 않는다. 토큰이 없을 때도 이 모듈은 안전하게 초기화되지만 원격
Logfire로는 아무 데이터도 보내지 않는다.
"""

from typing import Any

import logfire
from fastapi import FastAPI, Request, WebSocket


def configure_logfire() -> None:
    """Configure shared tracing before creating agents or MCP servers."""
    logfire.configure(
        service_name="job-matching-agent",
        send_to_logfire="if-token-present",
    )
    # Agent의 입력/출력에는 이력서와 공고 본문이 들어갈 수 있다.
    # 내용 대신 호출 순서, 시간, 토큰/비용 메타데이터만 기록한다.
    logfire.instrument_pydantic_ai(include_content=False)
    # 출처 API의 지연 시간과 오류만 기록한다. 요청/응답 본문은 남기지 않는다.
    logfire.instrument_httpx(capture_request_body=False, capture_response_body=False)


def _without_request_arguments(
    request: Request | WebSocket, attributes: dict[str, Any]
) -> dict[str, Any]:
    """Keep FastAPI request spans from recording parsed request bodies.

    ``/api/profile``의 ``resume_text``가 ``fastapi.arguments.values``에
    들어가는 것을 막는다. URL, 상태 코드, 시간 같은 HTTP 메타데이터는
    FastAPI 계측기가 계속 기록한다.
    """
    return {}


def instrument_fastapi(app: FastAPI) -> None:
    """Instrument one FastAPI app after ``configure_logfire``."""
    logfire.instrument_fastapi(
        app,
        request_attributes_mapper=_without_request_arguments,
    )
