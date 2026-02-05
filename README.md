# Local RAG Reply Assistant

A free, local RAG workflow that helps you identify relevant X posts, draft reply options, and log the replies you choose.

## What it does
- Scans for candidate posts (currently via a local sample feed).
- Filters by post age, impressions, and how often you've replied to an author.
- Generates three reply options:
  1. 200-280 character response
  2. Short meaningful comment
  3. A nice random alternative
- Shows a popup for selection and logs the reply with the original post.

## RAG inputs
- `data/reply_log.jsonl`: your past replies plus the post you replied to (appends automatically).
- `data/pdfs/`: PDFs with reference material.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### OCR prerequisites (optional)
If you enable OCR scanning, install Tesseract for your OS so `pytesseract` can access it.

## Model
The current reply drafting logic is heuristic/template-based (no hosted LLM), but any future LLM usage is intended for GPT-5.2-Codex (OpenAI). 

## Run
```bash
python -m app.main
```

## Customization
- Update `data/sample_posts.jsonl` with posts you want to test.
- Add PDFs to `data/pdfs/`.
- Adjust thresholds in `app/config.py`.
- To switch from the sample feed to OCR screen capture, set `use_ocr_scanner=True` in `app/config.py` and install the system Tesseract binary.

## Next steps
- Swap the sample feed with OCR-based screen capture or an X API integration.
- Replace the lightweight TF-IDF index with embeddings when you want richer retrieval.
