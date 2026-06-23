"""
PDF Intelligence service.

Responsibilities:
- Extract text from normal PDFs
- OCR fallback for image/scanned PDFs
- Chunk document text
- Build FAISS index
- Generate summaries
- Answer questions using RAG
"""

from pathlib import Path
import tempfile

import easyocr
import pdfplumber
from pdf2image import convert_from_path

from app.core.logging_config import logger
from app.db.mongodb import get_database
from app.services.faiss_service import faiss_service
from app.services.llm_service import llm_service
from app.utils.text_chunking import chunk_text


# OCR reader loads once
ocr_reader = easyocr.Reader(["en"], gpu=False)


def extract_pdf_text(file_path: Path) -> tuple[str, int]:
    """
    Extract text using pdfplumber.
    Returns (text, page_count)
    """
    full_text_parts = []

    with pdfplumber.open(file_path) as pdf:
        page_count = len(pdf.pages)

        for page in pdf.pages:
            page_text = page.extract_text() or ""
            full_text_parts.append(page_text)

    return "\n".join(full_text_parts), page_count


def extract_text_with_ocr(file_path: Path) -> str:
    """
    OCR fallback for scanned/image PDFs.
    """
    text_parts = []

    images = convert_from_path(str(file_path))

    for image in images:
        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        ) as temp_file:

            image.save(temp_file.name)

            results = ocr_reader.readtext(
                temp_file.name,
                detail=0
            )

            text_parts.append(
                " ".join(results)
            )

    return "\n".join(text_parts)


async def ingest_document(
    document_id: str,
    file_path: Path
) -> dict:

    full_text, page_count = extract_pdf_text(file_path)

    # OCR fallback
    if not full_text.strip():

        logger.warning(
            f"No text found in {document_id}. Using OCR fallback."
        )

        full_text = extract_text_with_ocr(file_path)

    logger.info(
        f"Document {document_id} extracted chars={len(full_text)}"
    )

    chunks = chunk_text(
        full_text,
        chunk_size=800,
        overlap=150
    )

    if chunks:

        await faiss_service.build_index(
            document_id,
            chunks
        )

        logger.info(
            f"Built index for {document_id} "
            f"with {len(chunks)} chunks"
        )

    else:

        logger.warning(
            f"No extractable text found in document {document_id}"
        )

    return {
        "page_count": page_count,
        "char_count": len(full_text),
        "chunk_count": len(chunks),
        "full_text": full_text,
    }

async def summarize_text(
    text: str,
    length: str = "medium",
    language: str = "en"
) -> str:

    length_guides = {
        "short": "in 2-3 sentences",
        "medium": "in a concise 1-2 paragraph summary",
        "long": "in a detailed multi-paragraph summary",
    }

    language_map = {
        "en": "English",
        "hi": "Hindi",
        "bn": "Bengali",
        "ta": "Tamil",
        "te": "Telugu",
        "mr": "Marathi",
    }

    target_language = language_map.get(
        language,
        "English"
    )

    guide = length_guides.get(
        length,
        length_guides["medium"]
    )

    excerpt = (
        text
        if len(text) < 12000
        else text[:6000] + "\n...\n" + text[-6000:]
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a document summarization assistant. "
                "Do not invent facts."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Summarize the following document {guide} "
                f"and return the summary in {target_language}.\n\n"
                f"{excerpt}"
            ),
        },
    ]

    return await llm_service.chat(
        messages,
        temperature=0.3
    )

async def answer_question_from_document(
    document_id: str,
    question: str,
    top_k: int = 4
) -> dict:

    retrieved = await faiss_service.search(
        document_id,
        question,
        top_k=top_k
    )

    if not retrieved:
        return {
            "answer": (
                "I couldn't find relevant content "
                "in this document."
            ),
            "sources": [],
        }

    context_block = "\n\n".join(
        f"[Excerpt {r['chunk_index']}]\n{r['text']}"
        for r in retrieved
    )

    messages = [
        {
            "role": "system",
            "content": (
                "Answer only using the provided excerpts. "
                "If unknown, say you don't know."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Document excerpts:\n{context_block}\n\n"
                f"Question: {question}"
            ),
        },
    ]

    answer = await llm_service.chat(
        messages,
        temperature=0.2
    )

    sources = [
        {
            "chunk_index": r["chunk_index"],
            "snippet": r["text"][:240],
            "score": r["score"],
        }
        for r in retrieved
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
    
async def generate_document_summary(
    document_id: str,
    length: str = "medium",
    language: str = "en"
) -> str:

    db = get_database()

    document = await db.documents.find_one(
        {"document_id": document_id}
    )

    if not document:
        raise ValueError("Document not found")

    file_path = Path(document["file_path"])

    full_text, _ = extract_pdf_text(file_path)

    if not full_text.strip():
        full_text = extract_text_with_ocr(file_path)

    summary = await summarize_text(
        full_text,
        length=length
    )

    await db.documents.update_one(
        {"document_id": document_id},
        {
            "$set": {
                "summary": summary
            }
        }
    )

    return summary