from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, List, Optional

from app.storage import ReplyRecord


@dataclass(frozen=True)
class DetectedPost:
    author: str
    text: str
    impressions: int
    timestamp: datetime


class ScreenScanner:
    def __init__(self, sample_posts: Path) -> None:
        self.sample_posts = sample_posts

    def scan(self) -> List[DetectedPost]:
        if not self.sample_posts.exists():
            return []
        posts: List[DetectedPost] = []
        with self.sample_posts.open("r", encoding="utf-8") as handle:
            for line in handle:
                payload = json.loads(line)
                posts.append(
                    DetectedPost(
                        author=payload["author"],
                        text=payload["text"],
                        impressions=int(payload.get("impressions", 0)),
                        timestamp=_parse_timestamp(payload["timestamp"]),
                    )
                )
        return posts



def filter_posts(
    posts: Iterable[DetectedPost],
    *,
    min_age: timedelta,
    max_age: timedelta,
    history: Iterable[ReplyRecord],
    max_recent_replies_per_author: int,
) -> List[DetectedPost]:
    now = datetime.now(timezone.utc)
    eligible: List[DetectedPost] = []
    for post in posts:
        age = now - post.timestamp
        if age < min_age or age > max_age:
            continue
        recent_replies = sum(1 for record in history if record.author == post.author)
        if recent_replies >= max_recent_replies_per_author:
            continue
        eligible.append(post)
    return eligible



def score_posts(posts: Iterable[DetectedPost]) -> List[DetectedPost]:
    return sorted(posts, key=lambda post: (post.impressions, post.timestamp), reverse=True)



def _parse_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
