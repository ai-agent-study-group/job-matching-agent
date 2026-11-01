import pytest
from pydantic_ai.models.test import TestModel

from src.adapter.inbound.agent.profile_agent import (
    create_profile_agent,
    extract_profile,
)
from src.domain.profile import Profile


@pytest.mark.asyncio
async def test_extract_profile():
    agent = create_profile_agent()

    with agent.override(model=TestModel()):
        profile = await extract_profile(
            "Data Analyst with Python and SQL experience.",
            agent=agent,
        )

    assert isinstance(profile, Profile)
    assert isinstance(profile.skills, list)
    assert isinstance(profile.job_titles, list)


@pytest.mark.asyncio
async def test_empty_resume():
    with pytest.raises(ValueError, match="Resume text cannot be empty"):
        await extract_profile("   ")


@pytest.mark.asyncio
async def test_profile_field_mapping():
    agent = create_profile_agent()

    expected = {
        "job_titles": ["Data Analyst"],
        "skills": ["Python", "SQL", "Power BI"],
        "years_of_experience": 3.0,
        "languages": ["Korean", "English"],
        "preferred_locations": ["Berlin"],
    }

    with agent.override(model=TestModel(custom_output_args=expected)):
        profile = await extract_profile(
            "Data Analyst with 3 years of experience. "
            "Skills: Python, SQL, Power BI. "
            "Languages: Korean, English. "
            "Preferred location: Berlin.",
            agent=agent,
        )

    assert profile.model_dump() == expected
