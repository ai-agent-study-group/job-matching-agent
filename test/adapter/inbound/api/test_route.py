from types import SimpleNamespace

from fastapi.testclient import TestClient

from domain.job import JobPosting
from domain.profile import Profile
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class FakeProfileAgent:
    async def run(self, resume_text: str):
        assert resume_text == "Python SQL Data Analyst Berlin"
        return SimpleNamespace(
            output=Profile(
                job_titles=["Data Analyst"],
                locations=["Berlin"],
            )
        )


class FakeSearchAgent:
    pass


def test_search_returns_job_postings(monkeypatch):
    expected_jobs = [
        JobPosting(
            source="arbeitsagentur",
            id="test-123",
            company="Example GmbH",
            title="Data Analyst",
            location="Berlin",
        )
    ]

    async def fake_run_search_agent(agent, profile):
        assert isinstance(agent, FakeSearchAgent)
        assert profile.job_titles == ["Data Analyst"]
        assert profile.locations == ["Berlin"]
        return expected_jobs

    monkeypatch.setattr(
        "adapter.inbound.api.route.run_search_agent",
        fake_run_search_agent,
    )

    app.state.profile_agent = FakeProfileAgent()
    app.state.search_agent = FakeSearchAgent()

    client = TestClient(app)
    response = client.post(
        "/api/search",
        json={"resume_text": "Python SQL Data Analyst Berlin"},
    )

    assert response.status_code == 200
    assert response.json() == [job.model_dump() for job in expected_jobs]


def test_search_rejects_blank_resume():
    client = TestClient(app)

    for resume_text in ["", "   "]:
        response = client.post(
            "/api/search",
            json={"resume_text": resume_text},
        )
        assert response.status_code == 422
