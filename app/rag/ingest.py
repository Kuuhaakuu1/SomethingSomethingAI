from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from pypdf import PdfReader


@dataclass(frozen=True)
class DocumentChunk:
    source: str
    text: str


def read_reply_pairs(reply_log: Path) -> List[DocumentChunk]:
    if not reply_log.exists():
        return []
    chunks: List[DocumentChunk] = []
    with reply_log.open("r", encoding="utf-8") as handle:
        for line in handle:
            chunks.append(DocumentChunk(source="reply_log", text=line.strip()))
    return chunks


def read_pdfs(pdf_dir: Path) -> List[DocumentChunk]:
    if not pdf_dir.exists():
        return []
    chunks: List[DocumentChunk] = []
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        reader = PdfReader(str(pdf_path))
        for page_index, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            for paragraph in _chunk_text(text):
                chunks.append(
                    DocumentChunk(
                        source=f"{pdf_path.name}#page={page_index + 1}",
                        text=paragraph,
                    )
                )
    return chunks


def _chunk_text(text: str, max_chars: int = 800) -> Iterable[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    paragraphs: List[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + max_chars, len(cleaned))
        paragraphs.append(cleaned[start:end])
        start = end
    return paragraphs
