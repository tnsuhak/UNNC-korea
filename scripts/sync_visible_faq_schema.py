#!/usr/bin/env python3
"""Synchronise FAQPage JSON-LD with the visible FAQ on masters pages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_RE = re.compile(
    r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)', re.S
)


def visible_faq(source: str) -> list[dict[str, object]]:
    doc = html.fromstring(source)
    details = doc.xpath(
        "//section[contains(concat(' ', normalize-space(@class), ' '), ' faq ')]//details"
    )
    entries: list[dict[str, object]] = []
    for detail in details:
        summary = detail.xpath("./summary")
        paragraphs = detail.xpath("./p")
        if not summary or not paragraphs:
            continue
        question = " ".join(summary[0].text_content().split())
        answer = " ".join(" ".join(p.text_content().split()) for p in paragraphs)
        entries.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
        )
    return entries


def sync_file(path: Path, write: bool) -> bool:
    source = path.read_text(encoding="utf-8")
    entries = visible_faq(source)
    if not entries:
        return False

    changed = False

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        try:
            payload = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        if payload.get("@type") != "FAQPage":
            return match.group(0)
        if payload.get("mainEntity") == entries:
            return match.group(0)
        payload["mainEntity"] = entries
        changed = True
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        return f"{match.group(1)}{encoded}{match.group(3)}"

    updated = SCRIPT_RE.sub(replace, source)
    if changed and write:
        path.write_text(updated, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="update mismatched JSON-LD")
    args = parser.parse_args()

    mismatches = [
        path.relative_to(ROOT)
        for path in sorted((ROOT / "masters").rglob("*.html"))
        if sync_file(path, args.write)
    ]
    if mismatches:
        action = "updated" if args.write else "mismatched"
        print(f"FAQ schema {action}: {len(mismatches)}")
        for path in mismatches:
            print(f"- {path}")
        return 0 if args.write else 1
    print("FAQ schema matches visible content on all masters pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
