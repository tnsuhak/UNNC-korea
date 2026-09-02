#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://unnc-korea.netlify.app/"
path = ROOT / "index.html"
text = path.read_text(encoding="utf-8")

# Make local image/media asset references safe when this HTML is rendered inside tnsuhak.com.
text = re.sub(
    r'(?P<prefix>\b(?:src|poster)=["\'])(?P<url>assets/[^"\']+)',
    lambda m: f"{m.group('prefix')}{BASE}{m.group('url')}",
    text,
)
text = re.sub(
    r'url\((?P<q>["\']?)(?P<url>assets/[^)"\']+)(?P=q)\)',
    lambda m: f"url({m.group('q')}{BASE}{m.group('url')}{m.group('q')})",
    text,
)

# Main-page links to UNNC detail pages should keep working when the main HTML is embedded on another domain.
text = re.sub(
    r'(?P<prefix>\bhref=["\'])(?P<url>unnc-[^"\']+\.html(?:#[^"\']*)?)',
    lambda m: f"{m.group('prefix')}{BASE}{m.group('url')}",
    text,
)

path.write_text(text, encoding="utf-8")
print("Converted UNNC homepage image/media and detail-page links to absolute public URLs")
