#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

text = INDEX.read_text(encoding="utf-8")

# Remove the large standalone guide directory. Detail pages remain; the homepage
# should surface them contextually beside the section the visitor is already reading.
text = re.sub(
    r"\n<!-- ===== INTERNAL GUIDES ===== -->.*?(?=\n<!-- ===== CALENDAR \(TUITION\) ===== -->)",
    "\n",
    text,
    flags=re.S,
)

context_css = r'''
  /* ---------- CONTEXTUAL DETAIL LINKS ---------- */
  .related-links{margin-top:22px;display:flex;align-items:center;justify-content:flex-end;gap:8px;flex-wrap:wrap}
  .related-label{font-family:'DM Mono',monospace;font-size:.63rem;letter-spacing:.12em;color:#98a2b3;margin-right:2px}
  .related-link{display:inline-flex;align-items:center;gap:7px;padding:8px 11px;border:1px solid #d9dee7;border-radius:3px;background:rgba(255,255,255,.72);color:var(--navy);font-size:.78rem;font-weight:700;line-height:1.4;transition:.2s}
  .related-link:hover{border-color:var(--gold);color:#8b6a1f;transform:translateY(-1px)}
  .related-link .arr{color:var(--gold)}
  #campus .related-label{color:#91a1b6}
  #campus .related-link{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.2);color:#eef3f9}
  #campus .related-link:hover{border-color:var(--gold);color:var(--gold-lt)}
  @media(max-width:560px){.related-links{justify-content:flex-start;margin-top:18px}.related-label{width:100%;margin-bottom:1px}.related-link{font-size:.75rem;padding:8px 10px}}
'''

# Replace now-unused directory-card CSS with the small contextual link style.
if "/* ---------- INTERNAL GUIDES ---------- */" in text:
    text = re.sub(
        r"\n\s*/\* ---------- INTERNAL GUIDES ---------- \*/.*?(?=\n\s*/\* ---------- FLOATING ---------- \*/)",
        "\n" + context_css + "\n",
        text,
        flags=re.S,
    )
elif "/* ---------- CONTEXTUAL DETAIL LINKS ---------- */" not in text:
    text = text.replace("  /* ---------- FLOATING ---------- */", context_css + "\n  /* ---------- FLOATING ---------- */")

# Make reruns safe.
text = re.sub(
    r"\n\s*<!-- CONTEXTUAL LINKS: [^>]+ -->\s*\n\s*<div class=\"wrap related-links\".*?</div>",
    "",
    text,
    flags=re.S,
)

links = {
    "information": [
        ("unnc-nottingham-degree-uk-campus.html", "노팅엄 학위·4+0·2+2"),
        ("unnc-how-study-english-teaching.html", "영어수업·수업방식"),
    ],
    "campus": [
        ("unnc-exchange-study-abroad.html", "교환학생·Study Abroad"),
        ("unnc-ningbo-china-life.html", "닝보 유학생활"),
    ],
    "major": [
        ("unnc-programmes-careers.html", "전공·졸업 후 진로"),
        ("unnc-career-support-further-study.html", "취업·대학원 진학 지원"),
    ],
    "calendar": [
        ("unnc-tuition-scholarships-2027.html", "학비·장학금·연간 비용 자세히"),
    ],
    "rooms": [
        ("unnc-accommodation-campus-life.html", "기숙사·캠퍼스 생활 자세히"),
    ],
    "admission": [
        ("unnc-admission-requirements-korea-2027.html", "2027 한국학생 입학조건"),
        ("unnc-application-documents-2027.html", "지원서류·지원 준비"),
    ],
}


def insert_links(html: str, section_id: str, items: list[tuple[str, str]]) -> str:
    anchors = "".join(
        f'<a class="related-link" href="{href}">{label}<span class="arr">→</span></a>'
        for href, label in items
    )
    block = (
        f'\n    <!-- CONTEXTUAL LINKS: {section_id} -->\n'
        f'    <div class="wrap related-links" aria-label="이 내용과 관련된 상세 가이드">'
        f'<span class="related-label">관련 글</span>{anchors}</div>\n'
    )
    pattern = re.compile(
        rf'(<section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>)(.*?)(</section>)',
        re.S,
    )
    match = pattern.search(html)
    if not match:
        raise SystemExit(f"Homepage section not found: {section_id}")
    return html[:match.start()] + match.group(1) + match.group(2) + block + match.group(3) + html[match.end():]


for section_id, items in links.items():
    text = insert_links(text, section_id, items)

# Guard against returning to a large directory block.
if 'id="guides"' in text or 'class="guide-grid' in text:
    raise SystemExit("Standalone guide directory still exists")

for section_id in links:
    if f"CONTEXTUAL LINKS: {section_id}" not in text:
        raise SystemExit(f"Contextual link block missing: {section_id}")

INDEX.write_text(text, encoding="utf-8")
print("Contextual homepage guide links applied")
