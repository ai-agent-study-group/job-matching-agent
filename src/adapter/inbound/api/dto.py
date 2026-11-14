"""API request DTOs."""

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class SearchRequestDTO(BaseModel):
    """Request body for searching jobs from resume text."""

    resume_text: Annotated[
        str,
        StringConstraints(
            # 공백시 422 출력
            strip_whitespace=True,
            min_length=1,
        ),
        Field(
            description="Resume as plain text",
            examples=[
                "Data analyst, 3 years of Python and SQL. Looking for a full-time job in Berlin."
            ],
        ),
    ]
