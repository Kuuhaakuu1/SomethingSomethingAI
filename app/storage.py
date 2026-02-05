from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class ReplyRecord:
    timestamp: str
    author: str
    post_text: str
    reply_text: str
    option_type: str
    impressions: int


def load_reply_history(log_path: Path) -> List[ReplyRecord]:
    if not log_path.exists():
        return []
    records: List[ReplyRecord] = []
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            records.append(
                ReplyRecord(
                    timestamp=payload["timestamp"],
                    author=payload["author"],
                    post_text=payload["post_text"],
                    reply_text=payload["reply_text"],
                    option_type=payload["option_type"],
                    impressions=int(payload.get("impressions", 0)),
                )
            )
    return records


def append_reply(
    log_path: Path,
    *,
    author: str,
    post_text: str,
    reply_text: str,
    option_type: str,
    impressions: int,
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "author": author,
        "post_text": post_text,
        "reply_text": reply_text,
        "option_type": option_type,
        "impressions": impressions,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def recent_reply_count(history: Iterable[ReplyRecord], author: str) -> int:
    return sum(1 for record in history if record.author == author)
