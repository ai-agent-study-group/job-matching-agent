from types import SimpleNamespace

from fastapi.testclient import TestClient
from pydantic import BaseModel
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models.function import FunctionModel

from adapter.inbound.agent.search import create_search_agent
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


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class FakeProfileAgent:
    async def run(self, resume_text: str):
        assert resume_text == "Data Analyst Berlin"
        return SimpleNamespace(
            output=Profile(
                job_titles=["Data Analyst"],
                locations=["Berlin"],
            )
        )


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
    registry = RegistryService({"fake": JobService(FakeSource())})

    search_agent = create_search_agent(
        FunctionModel(search_twice),
        MCPToolset(create_server(registry)),
    )

    monkeypatch.setattr(
        app.state,
        "profile_agent",
        FakeProfileAgent(),
        raising=False,
    )

    monkeypatch.setattr(
        app.state,
        "search_agent",
        search_agent,
        raising=False,
    )

    response = TestClient(app).post(
        "/api/search",
        json={"resume_text": "Data Analyst Berlin"},
    )

    assert response.status_code == 200
    assert response.json() == [POSTING.model_dump()]


def test_search_rejects_blank_resume():
    client = TestClient(app)

    for resume_text in ["", "   "]:
        response = client.post(
            "/api/search",
            json={"resume_text": resume_text},
        )
        assert response.status_code == 422
