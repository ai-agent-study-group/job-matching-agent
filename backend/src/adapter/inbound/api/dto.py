"""API request · response DTOs."""

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field

from domain.criteria import NonBlank


class ProfileRequestDTO(BaseModel):
    """Form body for extracting a profile from a resume."""

    # 모르는 키는 오류로 막음 (예: 예전 `resume_text`)
    model_config = ConfigDict(extra="forbid")

    # 파일이든 글이든 한 칸으로 받음. 글이 비어 있거나 공백뿐이면 422
    resume: UploadFile | NonBlank = Field(
        description="Resume as a PDF or DOCX file, or as plain text"
    )


class ErrorDTO(BaseModel):
    """Error response body."""

    detail: str = Field(description="What failed")
