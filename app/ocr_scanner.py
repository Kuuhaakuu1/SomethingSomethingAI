from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import List

try:
    import mss
    import mss.tools
    import pytesseract
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    mss = None
    pytesseract = None
    Image = None

from app.screen_scanner import DetectedPost


class OcrScreenScanner:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def scan(self) -> List[DetectedPost]:
        if mss is None or pytesseract is None or Image is None:
            return []
        self.output_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = self.output_dir / "latest_screen.png"
        with mss.mss() as capturer:
            monitor = capturer.monitors[1]
            shot = capturer.grab(monitor)
            mss.tools.to_png(shot.rgb, shot.size, output=str(screenshot_path))

        image = Image.open(screenshot_path)
        raw_text = pytesseract.image_to_string(image)
        cleaned = " ".join(raw_text.split())
        if not cleaned:
            return []
        return [
            DetectedPost(
                author="@screen_capture",
                text=cleaned,
                impressions=0,
                timestamp=datetime.now(timezone.utc),
            )
        ]
