from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from pydantic_ai.exceptions import (
    ModelAuthenticationError,
    ModelOverloadedError,
    ModelRateLimitError,
    ModelRequestTimeout,
    ModelTimeoutError,
    UnexpectedModelBehavior,
)
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models.function import FunctionModel

from adapter.inbound.agent.search import create_search_agent
from adapter.inbound.api.error import AGENT_ERROR_REASONS
from adapter.inbound.mcp.server import create_server
from domain.job import JobPosting
from domain.profile import Profile
from main import app
from port.outbound.source import JobSource
from service.job import JobService
from service.registry import RegistryService

POSTING = JobPosting(
    source="fake",
    id="test-123",
    company="Example GmbH",
    title="Data Analyst",
    location="Berlin",
)
PROFILE = Profile(job_titles=["Data Analyst"], locations=["Berlin"])
# 줄바꿈과 따옴표가 섞인 이력서. JSON으로 보낼 때 이스케이프돼도 agent에는 원문 그대로 가야 함
RESUME = 'Data Analyst\n3 years of "Python" and SQL\nBerlin'


def post_resume(resume: str):
    return TestClient(app).post("/api/profile", json={"resume_text": resume})


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class FakeProfileAgent:
    async def run(self, resume: str):
        assert resume == RESUME
        return SimpleNamespace(output=PROFILE)


class FailingAgent:
    """run()이 주어진 오류를 내는 agent."""

    def __init__(self, error: Exception):
        self.error = error

    async def run(self, prompt: str):
        raise self.error


def test_profile_returns_profile_from_resume(monkeypatch):
    monkeypatch.setattr(app.state, "profile_agent", FakeProfileAgent(), raising=False)

    response = post_resume(RESUME)

    assert response.status_code == 200
    assert response.json() == PROFILE.model_dump()


def test_profile_rejects_blank_resume():
    for resume in ["", "   "]:
        assert post_resume(resume).status_code == 422


@pytest.mark.parametrize(
    ("error", "status_code"),
    [
        (ModelRateLimitError("test", "rate limited"), 503),
        (ModelOverloadedError("test", "overloaded"), 503),
        (ModelTimeoutError("test", "timed out"), 504),
        (ModelRequestTimeout("test", 30), 504),
        (ModelAuthenticationError("test", "invalid key"), 502),
        (UnexpectedModelBehavior("no valid output after retries"), 502),
    ],
)
def test_profile_agent_failure_maps_to_status(monkeypatch, error, status_code):
    monkeypatch.setattr(app.state, "profile_agent", FailingAgent(error), raising=False)

    response = post_resume(RESUME)

    assert response.status_code == status_code
    reason = AGENT_ERROR_REASONS[status_code]
    assert response.json() == {"detail": f"Profile extraction failed. {reason}"}


class FakeRequestDTO(BaseModel):
    keywords: list[str]


class FakeSource(JobSource):
    def name(self) -> str:
        return "fake"

    def description(self) -> str:
        return "Fake job postings for testing"

    async def usage(self) -> type[BaseModel]:
        return FakeRequestDTO

    async def search(self, params: dict) -> list[JobPosting]:
        FakeRequestDTO.model_validate(params)
        return [POSTING]

    async def fetch(self, posting_id: str) -> JobPosting:
        return POSTING


def search_twice(messages, info):
    """Simulate an LLM calling search_jobs twice before finishing."""

    if sum(isinstance(m, ModelResponse) for m in messages) < 2:
        args = {
            "source": "fake",
            "params": {"keywords": ["Data Analyst"]},
        }
        return ModelResponse(parts=[ToolCallPart("search_jobs", args)])

    return ModelResponse(parts=[TextPart("done")])


def test_search_returns_postings_from_search_jobs(monkeypatch):
    registry = RegistryService([JobService(FakeSource())])

    search_agent = create_search_agent(
        FunctionModel(search_twice),
        MCPToolset(create_server(registry)),
    )

    monkeypatch.setattr(
        app.state,
        "search_agent",
        search_agent,
        raising=False,
    )

    response = TestClient(app).post("/api/search", json=PROFILE.model_dump())

    assert response.status_code == 200
    assert response.json() == [POSTING.model_dump()]


@pytest.mark.parametrize(
    ("error", "status_code"),
    [
        (ModelRateLimitError("test", "rate limited"), 503),
        (UnexpectedModelBehavior("Tool 'search_jobs' exceeded max retries count of 5"), 502),
    ],
)
def test_search_agent_failure_maps_to_status(monkeypatch, error, status_code):
    monkeypatch.setattr(app.state, "search_agent", FailingAgent(error), raising=False)

    response = TestClient(app).post("/api/search", json=PROFILE.model_dump())

    assert response.status_code == status_code
    reason = AGENT_ERROR_REASONS[status_code]
    assert response.json() == {"detail": f"Job search failed. {reason}"}
