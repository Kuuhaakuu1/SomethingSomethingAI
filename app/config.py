from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    data_dir: Path = Path("data")
    replies_log: Path = Path("data/reply_log.jsonl")
    sample_posts: Path = Path("data/sample_posts.jsonl")
    pdf_dir: Path = Path("data/pdfs")
    ocr_output_dir: Path = Path("data/ocr")
    use_ocr_scanner: bool = False
    min_post_age_minutes: int = 3
    max_post_age_minutes: int = 120
    max_recent_replies_per_author: int = 2
    scan_interval_seconds: int = 60
    top_k_candidates: int = 1


DEFAULT_CONFIG = AppConfig()
