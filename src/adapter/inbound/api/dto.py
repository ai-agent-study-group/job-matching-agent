"""API request · response DTOs."""

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class ProfileRequestDTO(BaseModel):
    """Request body for extracting a profile from resume text."""

    resume_text: Annotated[
        str,
        # 비어 있거나 공백뿐이면 422
        StringConstraints(strip_whitespace=True, min_length=1),
        Field(
            description="Resume as plain text",
            examples=[
                "Data analyst, 3 years of Python and SQL. Looking for a full-time job in Berlin.",
            ],
        ),
    ]


class ErrorDTO(BaseModel):
    """Error response body."""

    detail: str = Field(description="What failed")
