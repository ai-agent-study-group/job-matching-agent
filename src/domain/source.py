"""Source (공고 출처)"""

from pydantic import BaseModel, Field


class Source(BaseModel):
    """A job source the tools can search."""

    name: str = Field(description="Pass this as source to the other tools")
    description: str = Field(description="What postings this source has")
