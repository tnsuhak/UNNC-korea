#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "index.html"
text = path.read_text(encoding="utf-8")

PROD = "https://unnc-korea.netlify.app/"
PREVIEW = "https://deploy-preview-2--unnc-korea.netlify.app/"

# Keep canonical/schema/OG on the production URL, but load branch-only assets and
# detail pages from the stable Deploy Preview alias while the PR is under review.
text = text.replace(PROD + "assets/", PREVIEW + "assets/")
text = text.replace('href="' + PROD + "unnc-", 'href="' + PREVIEW + "unnc-")
text = text.replace("href='" + PROD + "unnc-", "href='" + PREVIEW + "unnc-")

path.write_text(text, encoding="utf-8")
print("Switched preview-only UNNC assets and detail links to Deploy Preview alias")
