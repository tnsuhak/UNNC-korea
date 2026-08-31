#!/usr/bin/env python3
from __future__ import annotations

import base64
import io
import pathlib
import re

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

DATA_URI_RE = re.compile(
    r"data:image/(?P<mime>png|jpeg|jpg|webp);base64,(?P<data>[A-Za-z0-9+/=]+)",
    re.IGNORECASE,
)

MIN_IMAGE_BYTES = 80_000
MAX_PHOTO_DIMENSION = 2560
WEBP_QUALITY = 85
MIN_SAVING_RATIO = 0.90


def encode_webp(raw: bytes) -> tuple[bytes, tuple[int, int]] | None:
    try:
        with Image.open(io.BytesIO(raw)) as source:
            if getattr(source, "is_animated", False):
                return None

            image = ImageOps.exif_transpose(source)
            width, height = image.size
            has_alpha = image.mode in ("RGBA", "LA") or "transparency" in image.info

            if max(width, height) > MAX_PHOTO_DIMENSION:
                scale = MAX_PHOTO_DIMENSION / max(width, height)
                image = image.resize(
                    (max(1, round(width * scale)), max(1, round(height * scale))),
                    Image.Resampling.LANCZOS,
                )

            if has_alpha:
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")

            out = io.BytesIO()
            image.save(out, format="WEBP", quality=WEBP_QUALITY, method=6)
            return out.getvalue(), image.size
    except Exception:
        return None


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    original_html_bytes = len(html.encode("utf-8"))

    image_number = 0
    optimized = 0
    original_image_bytes = 0
    optimized_image_bytes = 0
    details: list[str] = []

    def replace(match: re.Match[str]) -> str:
        nonlocal image_number, optimized, original_image_bytes, optimized_image_bytes
        image_number += 1
        raw = base64.b64decode(match.group("data"), validate=False)
        original_image_bytes += len(raw)

        if len(raw) < MIN_IMAGE_BYTES:
            optimized_image_bytes += len(raw)
            details.append(f"#{image_number}: kept {len(raw):,} B (small image)")
            return match.group(0)

        encoded = encode_webp(raw)
        if encoded is None:
            optimized_image_bytes += len(raw)
            details.append(f"#{image_number}: kept {len(raw):,} B (unsupported/animated)")
            return match.group(0)

        new_raw, dimensions = encoded
        if len(new_raw) >= len(raw) * MIN_SAVING_RATIO:
            optimized_image_bytes += len(raw)
            details.append(f"#{image_number}: kept {len(raw):,} B (no worthwhile saving)")
            return match.group(0)

        optimized += 1
        optimized_image_bytes += len(new_raw)
        encoded_b64 = base64.b64encode(new_raw).decode("ascii")
        details.append(
            f"#{image_number}: {len(raw):,} B -> {len(new_raw):,} B, "
            f"{dimensions[0]}x{dimensions[1]} WebP"
        )
        return f"data:image/webp;base64,{encoded_b64}"

    rewritten = DATA_URI_RE.sub(replace, html)
    new_html_bytes = len(rewritten.encode("utf-8"))

    if rewritten != html:
        INDEX.write_text(rewritten, encoding="utf-8")

    print(f"Embedded images found: {image_number}")
    print(f"Images optimized: {optimized}")
    print(f"Decoded image bytes: {original_image_bytes:,} -> {optimized_image_bytes:,}")
    print(f"index.html bytes: {original_html_bytes:,} -> {new_html_bytes:,}")
    if original_html_bytes:
        print(f"HTML size reduction: {(1 - new_html_bytes / original_html_bytes) * 100:.1f}%")
    for line in details:
        print(line)


if __name__ == "__main__":
    main()
