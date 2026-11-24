import asyncio
from io import BytesIO

import pytest
from docx import Document
from fastapi import HTTPException
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
from starlette.datastructures import UploadFile

from adapter.inbound.api.document_parser import document_to_text


def create_pdf() -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "Jane Doe")
    pdf.drawString(100, 730, "Python and SQL")
    pdf.save()
    return buffer.getvalue()


def create_docx() -> bytes:
    buffer = BytesIO()
    document = Document()
    document.add_paragraph("Jane Doe")
    document.add_paragraph("Python and SQL")
    document.save(buffer)
    return buffer.getvalue()


def create_upload_file(
    data: bytes,
    filename: str,
    content_type: str | None = None,
) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(data),
        headers={"content-type": content_type} if content_type else None,
    )


def test_pdf_extraction():
    file = create_upload_file(create_pdf(), "resume.pdf", "application/pdf")

    text = asyncio.run(document_to_text(file))

    assert "Jane Doe" in text
    assert "Python and SQL" in text


def test_docx_extraction():
    file = create_upload_file(
        create_docx(),
        "resume.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    text = asyncio.run(document_to_text(file))

    assert "Jane Doe" in text
    assert "Python and SQL" in text


def test_unsupported_file():
    file = create_upload_file(b"test", "resume.txt")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(document_to_text(file))

    assert exc_info.value.status_code == 415


def test_file_too_large():
    file = create_upload_file(b"a" * (5 * 1024 * 1024 + 1), "resume.pdf")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(document_to_text(file))

    assert exc_info.value.status_code == 413


def test_empty_file():
    file = create_upload_file(b"", "resume.pdf")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(document_to_text(file))

    assert exc_info.value.status_code == 422


def test_encrypted_pdf():
    buffer = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.encrypt("secret")
    writer.write(buffer)

    file = create_upload_file(
        buffer.getvalue(),
        "resume.pdf",
        "application/pdf",
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(document_to_text(file))

    assert exc_info.value.status_code == 422


def test_empty_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.save()

    file = create_upload_file(
        buffer.getvalue(),
        "empty.pdf",
        "application/pdf",
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(document_to_text(file))

    assert exc_info.value.status_code == 422


def test_invalid_docx():
    file = create_upload_file(b"invalid docx", "resume.docx")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(document_to_text(file))

    assert exc_info.value.status_code == 422


def test_mismatched_content_type():
    file = create_upload_file(
        create_pdf(),
        "resume.pdf",
        "application/msword",
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(document_to_text(file))

    assert exc_info.value.status_code == 415
