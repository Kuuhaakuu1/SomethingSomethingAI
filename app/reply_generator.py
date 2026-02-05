from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from app.rag.index import RagIndex


@dataclass(frozen=True)
class GeneratedReply:
    label: str
    text: str


def generate_replies(post_text: str, rag_index: RagIndex) -> List[GeneratedReply]:
    retrieved = rag_index.search(post_text, top_k=3)
    context_snippets = " ".join(chunk.text for chunk in retrieved)

    long_reply = _truncate(
        f"Interesting point. {post_text[:120]} Here's a related idea: {context_snippets[:120]}",
        280,
    )
    while len(long_reply) < 200:
        long_reply = _truncate(long_reply + " Appreciate you sharing.", 280)

    short_reply = _truncate(
        f"Great take. {context_snippets[:90] or 'Thanks for sharing.'}",
        120,
    )

    alternatives = [
        "Love the angle here—curious how you'll measure impact.",
        "This is a helpful reminder. Thanks for putting it out there.",
        "Thoughtful post. The emphasis on clarity really stands out.",
    ]
    random_reply = _truncate(random.choice(alternatives), 200)

    return [
        GeneratedReply(label="200-280 chars", text=long_reply),
        GeneratedReply(label="Short", text=short_reply),
        GeneratedReply(label="Random", text=random_reply),
    ]



def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text.strip()
    return text[: limit - 3].rstrip() + "..."
