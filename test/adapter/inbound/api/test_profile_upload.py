from io import BytesIO
from types import SimpleNamespace

import pytest
from docx import Document
from fastapi.testclient import TestClient

from domain.profile import Profile
from main import app


class FakeProfileAgent:
    async def run(self, resume_text: str):
        assert "Jane Doe" in resume_text
        return SimpleNamespace(
            output=Profile(
                job_titles=["Data Scientist"],
                locations=["Frankfurt"],
            )
        )


def create_docx():
    buffer = BytesIO()
    document = Document()
    document.add_paragraph("Jane Doe")
    document.add_paragraph("Python and SQL")
    document.save(buffer)
    return buffer.getvalue()


def test_profile_upload_success(monkeypatch):
    monkeypatch.setattr(
        app.state,
        "profile_agent",
        FakeProfileAgent(),
        raising=False,
    )

    response = TestClient(app).post(
        "/api/profile",
        files={
            "file": (
                "resume.docx",
                create_docx(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "job_titles": ["Data Scientist"],
        "locations": ["Frankfurt"],
    }


def test_profile_upload_unsupported_file():
    response = TestClient(app).post(
        "/api/profile",
        files={"file": ("resume.txt", b"some text", "text/plain")},
    )

    assert response.status_code == 415


def test_profile_upload_empty_document():
    buffer = BytesIO()
    document = Document()
    document.save(buffer)

    response = TestClient(app).post(
        "/api/profile",
        files={"file": ("empty.docx", buffer.getvalue())},
    )

    assert response.status_code == 422


def test_profile_upload_too_large():
    response = TestClient(app).post(
        "/api/profile",
        files={"file": ("resume.pdf", b"x" * (5 * 1024 * 1024 + 1))},
    )

    assert response.status_code == 413
