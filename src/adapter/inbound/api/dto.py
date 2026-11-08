"""API request DTOs."""

from typing import Annotated

from pydantic import BaseModel, StringConstraints


class SearchRequest(BaseModel):
    """Request body for searching jobs from resume text."""

    resume_text: Annotated[
        str,
        StringConstraints(
            # 공백시 422 출력
            strip_whitespace=True,
            min_length=1,
        ),
    ]
