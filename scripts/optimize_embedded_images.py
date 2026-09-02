#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT_DIR = ROOT / "assets" / "embedded"

DATA_URI_RE = re.compile(
    r"data:image/(?P<mime>png|jpeg|jpg|webp|gif|svg\+xml);base64,(?P<data>[A-Za-z0-9+/=\r\n\t ]+)",
    re.IGNORECASE,
)

EXT = {
    "png": "png",
    "jpeg": "jpg",
    "jpg": "jpg",
    "webp": "webp",
    "gif": "gif",
    "svg+xml": "svg",
}


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    original_html_bytes = len(html.encode("utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    seen: dict[str, str] = {}
    extracted: list[tuple[str, int]] = []
    image_number = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal image_number
        image_number += 1
        mime = match.group("mime").lower()
        compact_b64 = re.sub(r"\s+", "", match.group("data"))
        raw = base64.b64decode(compact_b64, validate=False)
        digest = hashlib.sha256(raw).hexdigest()[:16]

        if digest in seen:
            return seen[digest]

        rel = f"assets/embedded/{digest}.{EXT[mime]}"
        (ROOT / rel).write_bytes(raw)
        seen[digest] = rel
        extracted.append((rel, len(raw)))
        return rel

    rewritten = DATA_URI_RE.sub(replace, html)
    new_html_bytes = len(rewritten.encode("utf-8"))

    if rewritten != html:
        INDEX.write_text(rewritten, encoding="utf-8")

    print(f"Embedded image references found: {image_number}")
    print(f"Unique image files extracted: {len(extracted)}")
    print(f"index.html bytes: {original_html_bytes:,} -> {new_html_bytes:,}")
    if original_html_bytes:
        print(f"HTML size reduction: {(1 - new_html_bytes / original_html_bytes) * 100:.1f}%")
    print(f"Total extracted image bytes: {sum(size for _, size in extracted):,}")
    for path, size in extracted:
        print(f"- {path}: {size:,} B")


if __name__ == "__main__":
    main()
