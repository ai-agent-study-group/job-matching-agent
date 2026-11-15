from io import BytesIO

import pytest
from docx import Document
from reportlab.pdfgen import canvas

from adapter.inbound.api.document_parser import (
    document_to_text,
    InvalidDocumentError,
    UnsupportedDocumentError,
)


def create_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "Jane Doe")
    pdf.drawString(100, 730, "Python and SQL")
    pdf.save()
    return buffer.getvalue()


def create_docx():
    buffer = BytesIO()
    document = Document()
    document.add_paragraph("Jane Doe")
    document.add_paragraph("Python and SQL")
    document.save(buffer)
    return buffer.getvalue()


def test_pdf_extraction():
    text = document_to_text(create_pdf(), "resume.pdf")
    assert "Jane Doe" in text
    assert "Python and SQL" in text


def test_docx_extraction():
    text = document_to_text(create_docx(), "resume.docx")
    assert "Jane Doe" in text
    assert "Python and SQL" in text


def test_unsupported_file():
    with pytest.raises(UnsupportedDocumentError):
        document_to_text(b"test", "resume.txt")


def test_empty_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.save()

    with pytest.raises(InvalidDocumentError):
        document_to_text(buffer.getvalue(), "empty.pdf")
