"""
Extracts plain text from an uploaded resume file (PDF, DOCX, or TXT),
so the agent can work from a real uploaded file instead of requiring
the user to paste text manually.
"""

import io


def extract_resume_text(uploaded_file) -> str:
    """Takes a Streamlit UploadedFile and returns extracted plain text.
    Raises a ValueError with a user-friendly message on failure."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return _extract_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return _extract_docx(uploaded_file)
    elif filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF, DOCX, or TXT file."
        )


def _extract_pdf(uploaded_file) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(uploaded_file.read()))
    text_parts = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(text_parts).strip()

    if not text:
        raise ValueError(
            "Couldn't extract text from this PDF. It may be a scanned "
            "image rather than real text — try pasting the resume text "
            "manually instead."
        )
    return text


def _extract_docx(uploaded_file) -> str:
    import docx

    document = docx.Document(io.BytesIO(uploaded_file.read()))
    text = "\n".join(para.text for para in document.paragraphs).strip()

    if not text:
        raise ValueError("Couldn't extract text from this DOCX file.")
    return text
