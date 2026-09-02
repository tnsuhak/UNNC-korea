#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "index.html"
text = path.read_text(encoding="utf-8")
PREVIEW = "https://deploy-preview-2--unnc-korea.netlify.app/"
PROD = "https://unnc-korea.netlify.app/"
text = text.replace(PREVIEW + "assets/", PROD + "assets/")
text = text.replace('href="' + PREVIEW + "unnc-", 'href="' + PROD + "unnc-")
text = text.replace("href='" + PREVIEW + "unnc-", "href='" + PROD + "unnc-")
path.write_text(text, encoding="utf-8")
print("Finalized UNNC production asset and detail-page URLs")
