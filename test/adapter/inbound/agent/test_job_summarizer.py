"""Tests for Job Summarizer Agent."""

import asyncio

from pydantic_ai.models.test import TestModel

from adapter.inbound.agent.job_summarizer import (
    create_job_summarizer_agent,
)
from domain.jd import JD
from domain.job import JobPosting

POSTING = JobPosting(
    source="arbeitsagentur",
    id="12345",
    company="Example GmbH",
    title="Data Analyst",
    location="Berlin",
    description=(
        "We require Python, SQL and 2 years of experience. "
        "Power BI is preferred. German B2 is required."
    ),
)


def test_summarizer_returns_jd():
    agent = create_job_summarizer_agent("test")

    test_model = TestModel(
        custom_output_args={
            "source": "arbeitsagentur",
            "posting_id": "12345",
            "title": "Data Analyst",
            "company": "Example GmbH",
            "location": "Berlin",
            "required_skills": ["Python", "SQL"],
            "preferred_skills": ["Power BI"],
            "required_qualifications": [],
            "preferred_qualifications": [],
            "min_years_experience": 2,
            "work_mode": None,
            "required_soft_skills": ["Analytical thinking"],
            "preferred_soft_skills": [],
            "required_languages": ["German B2"],
            "preferred_languages": ["English"],
            "responsibilities": ["Data cleaning", "Data analysis"],
        }
    )

    with agent.override(model=test_model):
        result = asyncio.run(agent.run(POSTING.model_dump_json()))

    jd = result.output

    assert isinstance(jd, JD)
    assert jd.required_soft_skills == ["Analytical thinking"]
    assert jd.preferred_soft_skills == []
    assert jd.required_languages == ["German B2"]
    assert jd.preferred_languages == ["English"]
