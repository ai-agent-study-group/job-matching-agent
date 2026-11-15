from io import BytesIO
from zipfile import BadZipFile, ZipFile, is_zipfile

from docx import Document
from pypdf import PdfReader


class UnsupportedDocumentError(Exception):
    """Raised when the uploaded file type is not supported."""


class InvalidDocumentError(Exception):
    """Raised when the document is invalid or contains no text."""


def document_to_text(data: bytes, filename: str) -> str:
    """Extract text from PDF or DOCX documents."""

    extension = filename.rsplit(".", 1)[-1].lower()

    if extension not in {"pdf", "docx"}:
        raise UnsupportedDocumentError(
            "Only PDF and DOCX files are supported."
        )

    try:
        if extension == "pdf":
            reader = PdfReader(BytesIO(data), strict=False)

            if reader.is_encrypted:
                raise InvalidDocumentError(
                    "Encrypted PDF files are not supported."
                )

            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        else:
            buffer = BytesIO(data)

            if not is_zipfile(buffer):
                raise InvalidDocumentError("Invalid DOCX file.")

            with ZipFile(buffer) as archive:
                required_files = {
                    "[Content_Types].xml",
                    "word/document.xml",
                }

                if not required_files.issubset(archive.namelist()):
                    raise InvalidDocumentError("Invalid DOCX file.")

            document = Document(BytesIO(data))

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
            ]

            tables = [
                cell.text
                for table in document.tables
                for row in table.rows
                for cell in row.cells
            ]

            text = "\n".join(paragraphs + tables)

    except (UnsupportedDocumentError, InvalidDocumentError):
        raise

    except Exception as exc:
        raise InvalidDocumentError(
            "Could not extract text from the document."
        ) from exc

    if not text.strip():
        raise InvalidDocumentError(
            "No extractable text found in the document."
        )

    return text.strip()
