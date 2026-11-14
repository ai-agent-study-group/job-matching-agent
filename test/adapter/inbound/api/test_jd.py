"""Integration tests for POST /api/jd without external API calls."""

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from pydantic_ai.models.test import TestModel

from adapter.inbound.agent.job_summarizer import create_job_summarizer_agent
from adapter.inbound.mcp.server import create_server
from domain.job import JobPosting
from main import app
from port.outbound.source import JobSource
from service.job import JobService
from service.registry import RegistryService


class FakeSource(JobSource):
    def __init__(self, body: str | None):
        self.body = body

    def name(self) -> str:
        return "fake"

    def description(self) -> str:
        return "Fake job source"

    async def usage(self) -> type[BaseModel]:
        return BaseModel

    async def search(self, params: dict) -> list[JobPosting]:
        return []

    async def fetch(self, posting_id: str) -> JobPosting:
        if posting_id != "123":
            raise ValueError(f"No posting with id '{posting_id}'.")
        return JobPosting(
            source="fake",
            id="123",
            company="Example GmbH",
            title="Data Analyst",
            location="Berlin",
            description=self.body,
        )


def setup_api(monkeypatch, body: str | None):
    registry = RegistryService([JobService(FakeSource(body))])
    monkeypatch.setattr(app.state, "mcp_server", create_server(registry), raising=False)
    agent = create_job_summarizer_agent("test")
    monkeypatch.setattr(app.state, "job_summarizer_agent", agent, raising=False)
    return agent


def request_jd(posting_id: str = "123"):
    return TestClient(app).post("/api/jd", json={"source": "fake", "posting_id": posting_id})


def test_jd_api_returns_structured_jd(monkeypatch):
    agent = setup_api(monkeypatch, "Python and SQL required. Power BI preferred.")
    output = {
        "source": "wrong",
        "posting_id": "wrong",
        "title": "Wrong Title",
        "company": "Wrong Company",
        "location": "Wrong Location",
        "required_skills": ["Python", "SQL"],
        "preferred_skills": ["Power BI"],
        "required_soft_skills": ["Analytical thinking"],
        "preferred_soft_skills": [],
        "required_languages": ["German B1"],
        "preferred_languages": ["English"],
        "responsibilities": ["Data cleaning", "Data analysis"],
    }
    with agent.override(model=TestModel(custom_output_args=output)):
        response = request_jd()

    assert response.status_code == 200
    expected = output | {
        "source": "fake",
        "posting_id": "123",
        "title": "Data Analyst",
        "company": "Example GmbH",
        "location": "Berlin",
    }
    assert {key: response.json()[key] for key in expected} == expected


@pytest.mark.parametrize("description", [None, "", "   "])
def test_jd_api_rejects_empty_description(monkeypatch, description):
    setup_api(monkeypatch, description)
    assert request_jd().status_code == 422


def test_jd_api_handles_missing_job(monkeypatch):
    setup_api(monkeypatch, "Example description")
    assert request_jd("missing").status_code == 404
