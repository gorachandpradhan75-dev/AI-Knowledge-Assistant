"""Simple, dependency-free text chunking for RAG ingestion."""


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    """
    Splits text into overlapping chunks by character count, breaking on
    whitespace where possible so words aren't sliced in half.

    chunk_size/overlap are character counts (not tokens) — simple and
    predictable, and good enough for sentence-transformer context windows.
    """
    text = " ".join(text.split())  # normalize whitespace
    if not text:
        return []

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        if end < n:
            # try to break at the last space before `end` to avoid mid-word cuts
            last_space = text.rfind(" ", start, end)
            if last_space > start:
                end = last_space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= n:
            break
        start = max(end - overlap, start + 1)

    return chunks