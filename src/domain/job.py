"""JobPosting (공고 원문)"""

from pydantic import BaseModel, Field


class JobPosting(BaseModel):
    """A job posting from a source, converted to our common format."""

    source: str = Field(description="Source of the posting, e.g. arbeitsagentur")
    id: str = Field(description="Posting id within the source")
    company: str = Field(description="Company name")
    title: str = Field(description="Job title")
    location: str = Field(description="Location as written by the source")
    url: str | None = Field(
        default=None, description="Posting page URL; only set when a single posting is fetched"
    )
    description: str | None = Field(
        default=None,
        description="Posting body as plain text; only set when a single posting is fetched",
    )
