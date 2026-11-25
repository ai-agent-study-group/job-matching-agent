from io import BytesIO
from zipfile import ZipFile, is_zipfile

from docx import Document
from fastapi import HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from pypdf import PdfReader

MAX_FILE_SIZE = 5 * 1024 * 1024

SUPPORTED_TYPES = {
    "pdf": {"application/pdf", "application/octet-stream"},
    "docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/octet-stream",
    },
}


def _pdf_to_text(data: bytes) -> str:
    """Extract text from a PDF document."""
    reader = PdfReader(BytesIO(data), strict=False)

    if reader.is_encrypted:
        raise ValueError("Encrypted PDF files are not supported.")

    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _docx_to_text(data: bytes) -> str:
    """Extract text from a DOCX document."""
    buffer = BytesIO(data)

    if not is_zipfile(buffer):
        raise ValueError("Invalid DOCX file.")

    with ZipFile(BytesIO(data)) as archive:
        required_files = {
            "[Content_Types].xml",
            "word/document.xml",
        }

        if not required_files.issubset(archive.namelist()):
            raise ValueError("Invalid DOCX file.")

    document = Document(BytesIO(data))

    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    tables = [cell.text for table in document.tables for row in table.rows for cell in row.cells]

    return "\n".join(paragraphs + tables)


async def document_to_text(file: UploadFile) -> str:
    """Validate an uploaded PDF or DOCX file and extract its text."""
    filename = file.filename or ""
    extension = filename.rsplit(".", 1)[-1].lower()

    if extension not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Only PDF and DOCX files are supported.",
        )

    content_type = file.content_type
    if content_type and content_type not in SUPPORTED_TYPES[extension]:
        raise HTTPException(
            status_code=415,
            detail="File type does not match its extension.",
        )

    data = await file.read(MAX_FILE_SIZE + 1)

    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 5 MB.",
        )

    if not data:
        raise HTTPException(
            status_code=422,
            detail="The uploaded file is empty.",
        )

    try:
        # 글 뽑기는 await가 없는 동기 함수라 다른 스레드에서 돌림. 그동안 서버가 다른 요청을 받음
        text = await run_in_threadpool(_pdf_to_text if extension == "pdf" else _docx_to_text, data)

    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from the document.",
        ) from exc

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No extractable text found in the document.",
        )

    return text.strip()
