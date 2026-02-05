from __future__ import annotations

import time
from datetime import timedelta

from app.config import DEFAULT_CONFIG
from app.ocr_scanner import OcrScreenScanner
from app.rag.ingest import read_pdfs, read_reply_pairs
from app.rag.index import build_index
from app.reply_generator import generate_replies
from app.screen_scanner import ScreenScanner, filter_posts, score_posts
from app.storage import append_reply, load_reply_history
from app.ui import ReplyOption, show_reply_popup


def run_once() -> None:
    config = DEFAULT_CONFIG
    history = load_reply_history(config.replies_log)

    documents = read_reply_pairs(config.replies_log) + read_pdfs(config.pdf_dir)
    rag_index = build_index(documents)

    if config.use_ocr_scanner:
        ocr_scanner = OcrScreenScanner(config.ocr_output_dir)
        scanned_posts = ocr_scanner.scan()
    else:
        scanner = ScreenScanner(config.sample_posts)
        scanned_posts = scanner.scan()
    min_age = timedelta(minutes=0 if config.use_ocr_scanner else config.min_post_age_minutes)
    eligible = filter_posts(
        scanned_posts,
        min_age=min_age,
        max_age=timedelta(minutes=config.max_post_age_minutes),
        history=history,
        max_recent_replies_per_author=config.max_recent_replies_per_author,
    )
    ranked = score_posts(eligible)

    for post in ranked[: config.top_k_candidates]:
        options = [ReplyOption(label=reply.label, text=reply.text) for reply in generate_replies(post.text, rag_index)]
        chosen = show_reply_popup(post.text, options)
        if chosen:
            append_reply(
                config.replies_log,
                author=post.author,
                post_text=post.text,
                reply_text=chosen.text,
                option_type=chosen.label,
                impressions=post.impressions,
            )


def main() -> None:
    config = DEFAULT_CONFIG
    while True:
        run_once()
        time.sleep(config.scan_interval_seconds)


if __name__ == "__main__":
    main()
