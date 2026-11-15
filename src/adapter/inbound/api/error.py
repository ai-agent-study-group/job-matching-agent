"""/api 오류 응답: agent 실패를 HTTP 오류로 바꾸고, 같은 내용을 Swagger에 적음."""

import logging

from fastapi import HTTPException, status
from pydantic_ai.exceptions import (
    AgentRunError,
    ModelRateLimitError,
    ModelRequestTimeout,
    ModelTimeoutError,
    ModelUnavailableError,
)

from adapter.inbound.api.dto import ErrorDTO

logger = logging.getLogger(__name__)

# agent 실패의 상태 코드별 원인. 응답 detail과 Swagger 설명이 같이 씀.
# LLM 제공자의 오류 원문은 내부 정보가 섞여 있어 내보내지 않고 서버 로그에만 남김
AGENT_ERROR_REASONS = {
    status.HTTP_502_BAD_GATEWAY: "The agent failed for another reason, such as an LLM error",
    status.HTTP_503_SERVICE_UNAVAILABLE: "The LLM is rate limited or overloaded. Try again later",
    status.HTTP_504_GATEWAY_TIMEOUT: "The LLM did not respond in time. Try again later",
}


def agent_error(error: AgentRunError, step: str) -> HTTPException:
    """agent 실패를 로그에 남기고 HTTP 오류로 바꿈. 잠시 뒤 다시 하면 될 수 있는 LLM 실패는 503 · 504."""
    logger.error(step, exc_info=error)
    if isinstance(error, (ModelTimeoutError, ModelRequestTimeout)):
        code = status.HTTP_504_GATEWAY_TIMEOUT
    # 과부하(ModelOverloadedError)는 ModelUnavailableError에 포함됨
    elif isinstance(error, (ModelRateLimitError, ModelUnavailableError)):
        code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        code = status.HTTP_502_BAD_GATEWAY
    return HTTPException(code, f"{step}. {AGENT_ERROR_REASONS[code]}")


def agent_errors(step: str) -> dict:
    """Swagger에 적을 agent 실패 응답. step은 실패한 단계 (예: "Job search failed")."""
    return {
        code: {
            "model": ErrorDTO,
            "description": reason,
            "content": {"application/json": {"example": {"detail": f"{step}. {reason}"}}},
        }
        for code, reason in AGENT_ERROR_REASONS.items()
    }
