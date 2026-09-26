#!/usr/bin/env python3
"""Deterministic QA for the complete UNNC masters section.

Runs the Taught/MRes data validators, then checks every masters HTML page for
SEO basics, structured data, links, sitemap coverage, local assets and the
content rules that keep the pages consistent with data/unnc-masters-2027.json
and data/unnc-mres-2027.json.

Usage: python3 scripts/validate_masters_site.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
MASTERS_ROOT = ROOT / "masters"
SITE_ORIGIN = "https://unnc-korea.netlify.app"
EXPECTED_OG_IMAGE = "/assets/embedded/0cddcf1b60ebd2e7.webp"
EXPECTED_FAVICON = "/favicon.svg"
EXPECTED_HTML_COUNT = 40
EXPECTED_TAUGHT_DETAILS = 26
EXPECTED_MRES_DETAILS = 9

errors: list[str] = []
warnings: list[str] = []


def fail(path: Path | str, message: str) -> None:
    errors.append(f"{path}: {message}")


def warn(path: Path | str, message: str) -> None:
    warnings.append(f"{path}: {message}")


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def public_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def local_target_from_url(url_path: str) -> Path:
    clean = unquote(url_path).lstrip("/")
    target = ROOT / clean
    if url_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


# Research/attribution voice that SITE_RULES.md and policies.yaml keep out of ordinary pages.
ATTRIBUTION_PATTERNS = (
    r"공식 홈페이지에 따르면", r"홈페이지에 따르면", r"브로셔에 따르면", r"모집자료에 따르면", r"자료를 보면",
    r"공식 자료 기준", r"공식\s?(과정\s?)?페이지(는|의|에|가)", r"공식 안내(상|는)", r"공식 PGR 자료",
)
DURATION_RE = re.compile(r"(12|21|24)\s*개월")
GPA_SINGLE_CUTOFF_RE = re.compile(r"(2\.9|3\.1|3\.3|3\.5|3\.7)\s*(이면|만 넘으면|이상이면 (합격|가능))")
STAT_MISCOUNT_RE = re.compile(r"21개월\s*1개|1개\s*21개월|24개월\s*1개|1개\s*24개월|21개월 과정인 하나")


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[?!])|(?<=[다요]\.)|(?<=\.)\s", text) if s.strip()]


def check_content(page: Path, rel: Path, doc, visible: str, schemas: list[dict]) -> None:
    path = public_path(page)
    for pattern in ATTRIBUTION_PATTERNS:
        match = re.search(pattern, visible)
        if match:
            fail(rel, f"source-attribution phrasing in visible copy: {match.group(0)!r}")
    if STAT_MISCOUNT_RE.search(visible):
        fail(rel, "duration statistics miscount (Computer Science and Professional Accounting are 21 months)")
    for sentence in sentences(visible):
        if GPA_SINGLE_CUTOFF_RE.search(sentence) and not sentence.endswith("?"):
            fail(rel, f"Korean GPA collapsed into a single cutoff: {sentence[:80]!r}")
    for sentence in sentences(visible):
        if ("장학" in sentence and re.search(r"(전체|2년|두 해|전 기간)\s*(과정\s*)?학비", sentence)
                and not sentence.endswith("?") and not re.search(r"아닙니다|않습니다|아니라|첫해", sentence)):
            fail(rel, f"scholarship described beyond first-year tuition: {sentence[:80]!r}")

    course = TAUGHT_BY_PATH.get(path)
    if course:
        check_taught_detail(rel, doc, visible, schemas, course)
    mres = MRES_BY_PATH.get(path)
    if mres:
        check_mres_detail(rel, doc, visible, schemas, mres)
    if path.startswith("/masters/mres/"):
        for sentence in sentences(visible):
            if re.search(r"100%|50%", sentence) and not sentence.endswith("?") and not re.search(r"Taught|PGT", sentence):
                fail(rel, f"Taught 100%/50% scholarship shown on MRes page without Taught context: {sentence[:80]!r}")
        if re.search(r"2\.9\s*/\s*3\.3|3\.3\s*/\s*3\.7|3\.1\s*/\s*3\.5", visible):
            fail(rel, "Taught South Korea GPA table copied onto MRes page")


def check_taught_detail(rel: Path, doc, visible: str, schemas: list[dict], course: dict) -> None:
    if not doc.xpath('//nav[contains(@class,"nav")]//a[@href="/masters/mres/"]'):
        fail(rel, "Taught detail desktop navigation missing MRes link")
    if not doc.xpath('//*[@id="mobileNav"]//a[@href="/masters/mres/"]'):
        fail(rel, "Taught detail mobile navigation missing MRes link")
    months = course["duration_months"]
    h1 = norm(doc.xpath("//h1")[0].text_content()) if doc.xpath("//h1") else ""
    if course["name"] not in h1 and course["name"] != "Teaching English to Speakers of Other Languages":
        fail(rel, f"H1 {h1!r} does not contain programme name {course['name']!r}")
    other = {m for m in map(int, DURATION_RE.findall(visible))} - {months}
    if other:
        fail(rel, f"{months}-month programme page mentions other durations {sorted(other)}")
    summary = norm(" ".join(n.text_content() for n in doc.xpath('//*[@class="programme-pills" or @class="programme-summary"]')))
    if f"{months}개월" not in summary:
        fail(rel, f"hero/summary missing {months}개월")
    ielts = "6.0" if course["english_profile"] == "lower_6_0" else "6.5"
    if f"IELTS {ielts}" not in summary:
        fail(rel, f"hero/summary missing IELTS {ielts}")
    pending = course["intake_2027_status"].startswith("pending")
    if pending:
        if "2027 확인중" not in summary:
            fail(rel, "pending 2027 intake must show '2027 확인중' in hero/summary")
        if "2027년 9월" in summary:
            fail(rel, "pending 2027 intake shown as 2027년 9월 in hero/summary")
        for sentence in sentences(visible):
            if "2027년 9월" in sentence and not sentence.endswith("?"):
                fail(rel, f"pending intake page asserts 2027년 9월: {sentence[:80]!r}")
    elif "2027년 9월" not in summary:
        fail(rel, "confirmed recurring intake should show 2027년 9월 in hero/summary")
    amount = f"{course['tuition']['amount_per_year']:,} RMB"
    if amount not in visible:
        fail(rel, f"tuition {amount} missing")
    if "2027 학비" not in visible or not re.search(r"아직 (?:공개되지 않았습니다|미공개)", visible):
        fail(rel, "2027 tuition pending status missing")
    if "장학금 100%·50%" in visible:
        fail(rel, "programme detail page still exposes numeric scholarship teaser")
    if "학비·지원제도 확인" not in visible:
        fail(rel, "NEXT cost card must use '학비·지원제도 확인'")
    if "지원 가능성과 2027 장학금 준비" in visible:
        fail(rel, "consultation CTA still uses scholarship-preparation wording")

    expected_rhythm = (
        ("GRADUATE CAPABILITIES", True),
        ("CAREERS", False),
        ("TUITION", True),
        ("NEXT", False),
        ("FAQ", True),
    )
    for label, should_alt in expected_rhythm:
        sections = doc.xpath(
            f'//section[.//div[contains(concat(" ", normalize-space(@class), " "), " label ") and normalize-space()="{label}"]]'
        )
        if len(sections) != 1:
            fail(rel, f"expected one {label} section, found {len(sections)}")
            continue
        classes = (sections[0].get("class") or "").split()
        is_alt = "alt" in classes
        if is_alt != should_alt:
            fail(rel, f"{label} section background rhythm incorrect: classes={classes}")
    needs_portfolio = any("portfolio" in r.lower() for r in course.get("additional_requirements", []))
    if not needs_portfolio and "포트폴리오" in visible:
        fail(rel, "portfolio mentioned but not in data additional_requirements")
    if needs_portfolio and "포트폴리오" not in visible:
        fail(rel, "portfolio required by data but not mentioned")
    for req, token in (("HSK 4", "HSK 4"), ("HSK 6", "HSK 6"), ("Interview with course admissions tutor required", "인터뷰")):
        if any(req in r for r in course.get("additional_requirements", [])) and token not in visible:
            fail(rel, f"additional requirement {req!r} not shown")
    courses = [s for s in schemas if s.get("@type") == "Course"]
    if courses and course["name"] not in courses[0].get("name", "") and "TESOL" not in courses[0].get("name", ""):
        fail(rel, f"Course schema name {courses[0].get('name')!r} differs from data")


def check_mres_detail(rel: Path, doc, visible: str, schemas: list[dict], mres: dict) -> None:
    pills = norm(" ".join(n.text_content() for n in doc.xpath('//*[@class="mres-pills"]')))
    for token in ("12개월", "2월·9월", "IELTS 6.0"):
        if token not in pills:
            fail(rel, f"MRes hero pills missing {token!r}")
    for token in ("5.5", "지도교수", "Research Proposal", "1,000~3,000", "2025/26", "130,000 RMB", "2027 학비"):
        if token not in visible:
            fail(rel, f"MRes page missing {token!r}")
    if "아직 미공개" not in visible:
        fail(rel, "MRes 2027 tuition pending status missing")
    for stale in ("TUITION & FUNDING", "2027 MRes 전용 장학금", "100%·50%"):
        if stale in visible:
            fail(rel, f"MRes detail page contains stale scholarship/funding copy: {stale!r}")

    expected_rhythm = (
        ("RESEARCH OVERVIEW", False),
        ("ENTRY REQUIREMENTS", True),
        ("RESEARCH THEMES", False),
        ("COURSE STRUCTURE", True),
        ("2027 ENTRY", False),
        ("TUITION", True),
        ("NEXT", False),
        ("FAQ", True),
    )
    for label, should_alt in expected_rhythm:
        sections = doc.xpath(
            f'//section[.//div[contains(concat(" ", normalize-space(@class), " "), " label ") and normalize-space()="{label}"]]'
        )
        if len(sections) != 1:
            fail(rel, f"expected one {label} section, found {len(sections)}")
            continue
        classes = (sections[0].get("class") or "").split()
        is_alt = "alt" in classes
        if is_alt != should_alt:
            fail(rel, f"{label} section background rhythm incorrect: classes={classes}")
    if re.search(r"[A-Za-z]{4,}(?: [A-Za-z,/&()-]+){6,}\.", norm(doc.xpath("//h1/following-sibling::p[1]")[0].text_content()) if doc.xpath("//h1/following-sibling::p[1]") else ""):
        fail(rel, "MRes hero lead is English-only")


for validator in ("validate_unnc_masters_data.py", "validate_unnc_mres_data.py"):
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / validator)], capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"scripts/{validator}", (result.stdout + result.stderr).strip().splitlines()[-1] if (result.stdout + result.stderr).strip() else "failed")

TAUGHT = json.loads((ROOT / "data" / "unnc-masters-2027.json").read_text(encoding="utf-8"))
MRES = json.loads((ROOT / "data" / "unnc-mres-2027.json").read_text(encoding="utf-8"))
TAUGHT_BY_PATH = {c["detail_path"]: c for c in TAUGHT["courses"]}
MRES_BY_PATH = {c["detail_path"]: c for c in MRES["programmes"]}

pages = sorted(MASTERS_ROOT.rglob("*.html"))
if len(pages) != EXPECTED_HTML_COUNT:
    fail("masters", f"expected {EXPECTED_HTML_COUNT} HTML pages, found {len(pages)}")

taught_details = sorted((MASTERS_ROOT / "programmes").glob("*.html"))
mres_details = sorted((MASTERS_ROOT / "mres").glob("*-mres.html"))
if len(taught_details) != EXPECTED_TAUGHT_DETAILS:
    fail("masters/programmes", f"expected {EXPECTED_TAUGHT_DETAILS} detail pages, found {len(taught_details)}")
if len(mres_details) != EXPECTED_MRES_DETAILS:
    fail("masters/mres", f"expected {EXPECTED_MRES_DETAILS} detail pages, found {len(mres_details)}")

titles: defaultdict[str, list[str]] = defaultdict(list)
descriptions: defaultdict[str, list[str]] = defaultdict(list)
canonicals: defaultdict[str, list[str]] = defaultdict(list)
parsed_pages: dict[Path, html.HtmlElement] = {}

for page in pages:
    rel = page.relative_to(ROOT)
    try:
        doc = html.fromstring(page.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(rel, f"HTML parse failed: {exc}")
        continue
    parsed_pages[page] = doc

    if doc.get("lang") != "ko":
        fail(rel, f"html lang must be ko, found {doc.get('lang')!r}")

    h1s = doc.xpath("//h1")
    if len(h1s) != 1:
        fail(rel, f"expected exactly one H1, found {len(h1s)}")

    title = norm("".join(doc.xpath("//title/text()")))
    if not title:
        fail(rel, "missing title")
    else:
        titles[title].append(str(rel))

    desc_nodes = doc.xpath('//meta[translate(@name,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="description"]/@content')
    description = norm(desc_nodes[0]) if desc_nodes else ""
    if not description:
        fail(rel, "missing meta description")
    else:
        descriptions[description].append(str(rel))
        if len(description) < 60:
            fail(rel, f"meta description too short ({len(description)} chars)")

    robots = [v.lower().replace(" ", "") for v in doc.xpath('//meta[translate(@name,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="robots"]/@content')]
    if not robots or not any("index" in v and "follow" in v and "noindex" not in v for v in robots):
        fail(rel, f"robots must be index,follow; found {robots or 'missing'}")

    expected_canonical = SITE_ORIGIN + public_path(page)
    canonical_nodes = doc.xpath('//link[translate(@rel,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="canonical"]/@href')
    if len(canonical_nodes) != 1:
        fail(rel, f"expected one canonical, found {len(canonical_nodes)}")
        canonical = ""
    else:
        canonical = canonical_nodes[0]
        canonicals[canonical].append(str(rel))
        if canonical != expected_canonical:
            fail(rel, f"canonical mismatch: {canonical!r}, expected {expected_canonical!r}")

    favicon = doc.xpath('//link[contains(concat(" ", normalize-space(@rel), " "), " icon ")]/@href')
    if EXPECTED_FAVICON not in favicon:
        fail(rel, f"missing central favicon {EXPECTED_FAVICON}")

    og_required = {
        "og:title": None,
        "og:description": None,
        "og:url": canonical,
        "og:image": SITE_ORIGIN + EXPECTED_OG_IMAGE,
    }
    for prop, expected in og_required.items():
        values = doc.xpath(f'//meta[@property="{prop}"]/@content')
        if len(values) != 1 or not norm(values[0]):
            fail(rel, f"missing or duplicate {prop}")
        elif expected is not None and values[0] != expected:
            fail(rel, f"{prop} mismatch: {values[0]!r}, expected {expected!r}")

    twitter = doc.xpath('//meta[@name="twitter:card"]/@content')
    if twitter != ["summary_large_image"]:
        fail(rel, f"twitter:card must be summary_large_image; found {twitter}")

    schema_nodes = doc.xpath('//script[@type="application/ld+json"]/text()')
    schemas: list[dict] = []
    for index, raw in enumerate(schema_nodes, start=1):
        try:
            value = json.loads(raw)
            schemas.extend(value if isinstance(value, list) else [value])
        except Exception as exc:
            fail(rel, f"JSON-LD #{index} invalid: {exc}")
    schema_types = [s.get("@type") for s in schemas if isinstance(s, dict)]
    if "BreadcrumbList" not in schema_types:
        fail(rel, "missing BreadcrumbList schema")
    is_detail = page in taught_details or page in mres_details
    if is_detail and "Course" not in schema_types:
        fail(rel, "programme detail page missing Course schema")
    if not is_detail and "Course" in schema_types:
        fail(rel, "non-programme page must not use Course schema")

    for schema in schemas:
        if not isinstance(schema, dict):
            continue
        if schema.get("@type") == "Course" and schema.get("url") != canonical:
            fail(rel, f"Course schema URL differs from canonical: {schema.get('url')!r}")
        if schema.get("@type") == "BreadcrumbList":
            items = schema.get("itemListElement", [])
            if not items or items[-1].get("item") != canonical:
                fail(rel, "BreadcrumbList final item must equal canonical")

    visible_faq = []
    for details in doc.xpath('//section[contains(concat(" ", normalize-space(@class), " "), " faq ")]//details'):
        questions = details.xpath("./summary")
        answers = details.xpath("./p[1]")
        if questions and answers:
            visible_faq.append((norm(questions[0].text_content()), norm(answers[0].text_content())))
    faq_schemas = [s for s in schemas if isinstance(s, dict) and s.get("@type") == "FAQPage"]
    if visible_faq and not faq_schemas:
        fail(rel, "visible FAQ exists but FAQPage schema is missing")
    if faq_schemas:
        schema_faq = []
        for item in faq_schemas[0].get("mainEntity", []):
            schema_faq.append((norm(item.get("name", "")), norm(item.get("acceptedAnswer", {}).get("text", ""))))
        if schema_faq != visible_faq:
            fail(rel, f"FAQ schema does not exactly match visible FAQ ({len(schema_faq)} schema vs {len(visible_faq)} visible)")

    ids = set(doc.xpath('//*[@id]/@id'))
    for anchor in doc.xpath("//a[@href]"):
        href = norm(anchor.get("href"))
        label = norm(anchor.text_content())
        if not href or href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https"}:
            if parsed.netloc == "unnc-korea.netlify.app":
                target = local_target_from_url(parsed.path)
                if not target.exists():
                    fail(rel, f"broken absolute internal link {href}")
            else:
                combined = f"{label} {href}".lower()
                if any(term in combined for term in ("application portal", "how to apply", "how-to-apply", "/apply", "apply now", "apply.aspx", "application.aspx")):
                    fail(rel, f"direct application/how-to-apply external link exposed: {href}")
                if anchor.get("target") == "_blank" and "noopener" not in (anchor.get("rel") or ""):
                    fail(rel, f"target=_blank link missing rel=noopener: {href}")
            continue
        if href.startswith("#"):
            if href[1:] not in ids:
                fail(rel, f"broken same-page anchor {href}")
            continue
        target_path = parsed.path
        if target_path.startswith("/"):
            target = local_target_from_url(target_path)
        else:
            target = (page.parent / target_path).resolve()
            if target_path.endswith("/"):
                target = target / "index.html"
        if not target.exists():
            fail(rel, f"broken internal link {href}")
            continue
        if parsed.fragment and target.suffix == ".html":
            try:
                target_doc = parsed_pages.get(target)
                if target_doc is None:
                    target_doc = html.fromstring(target.read_text(encoding="utf-8"))
                if parsed.fragment not in set(target_doc.xpath('//*[@id]/@id')):
                    fail(rel, f"broken target fragment {href}")
            except Exception as exc:
                fail(rel, f"could not verify target fragment {href}: {exc}")

    body_copy = html.fromstring(html.tostring(doc.xpath("//body")[0], encoding="unicode"))
    for node in body_copy.xpath("//script|//style"):
        node.drop_tree()
    visible = norm(body_copy.text_content())
    visible_text = visible.lower()
    if "자료 출처" in visible_text or "공식 확인 자료" in visible_text or "official sources" in visible_text:
        fail(rel, "visible source box/label found")
    check_content(page, rel, doc, visible, schemas)

    for asset in doc.xpath('//link[@href]/@href | //script[@src]/@src | //img[@src]/@src'):
        parsed = urlparse(asset)
        if parsed.scheme or asset.startswith("//") or asset.startswith("data:"):
            continue
        target = local_target_from_url(parsed.path) if parsed.path.startswith("/") else (page.parent / parsed.path).resolve()
        if not target.exists():
            fail(rel, f"missing local asset {asset}")


# Finder cards on /masters/programmes.html must mirror the Taught data file.
finder_page = MASTERS_ROOT / "programmes.html"
finder = parsed_pages.get(finder_page)
if finder is not None:
    cards = finder.xpath('//article[contains(concat(" ", normalize-space(@class), " "), " programme-card ")]')
    if len(cards) != len(TAUGHT["courses"]):
        fail("masters/programmes.html", f"expected {len(TAUGHT['courses'])} finder cards, found {len(cards)}")
    by_href = {}
    for card in cards:
        hrefs = card.xpath(".//h2/a/@href")
        if hrefs:
            by_href[hrefs[0]] = card
    for course in TAUGHT["courses"]:
        card = by_href.get(course["detail_path"])
        where = f"masters/programmes.html card {course['name']!r}"
        if card is None:
            fail(where, "missing or not linked to detail_path")
            continue
        if card.get("data-duration") != str(course["duration_months"]):
            fail(where, f"data-duration {card.get('data-duration')} != {course['duration_months']}")
        ielts = "6.0" if course["english_profile"] == "lower_6_0" else "6.5"
        if card.get("data-ielts") != ielts:
            fail(where, f"data-ielts {card.get('data-ielts')} != {ielts}")
        if card.get("data-degree") != course["degree"]:
            fail(where, f"data-degree {card.get('data-degree')} != {course['degree']}")
        text = norm(card.text_content())
        pending = course["intake_2027_status"].startswith("pending")
        if pending != bool(card.xpath('.//*[contains(@class, "pending")]')):
            fail(where, "2027 확인중 badge does not match data intake status")
        tags = [norm(t.text_content()) for t in card.xpath('.//div[@class="extra-tags"]/b')]
        reqs = " ".join(course.get("additional_requirements", [])).lower()
        if ("portfolio" in reqs) != any("포트폴리오" in tag for tag in tags):
            fail(where, f"portfolio tag {tags} does not match data")
        if "interview with course admissions tutor required" in reqs and "인터뷰 필수" not in tags:
            fail(where, f"mandatory interview should be tagged 인터뷰 필수, found {tags}")
        if "인터뷰 필수" in tags and "interview with course admissions tutor required" not in reqs:
            fail(where, "인터뷰 필수 tag without mandatory interview in data")
        amount = f"RMB {course['tuition']['amount_per_year']:,}"
        if amount not in text:
            fail(where, f"tuition {amount} missing")
    counts = Counter(c["duration_months"] for c in TAUGHT["courses"])
    stats = norm(" ".join(n.text_content() for n in finder.xpath('//*[@class="list-hero-stats"]')))
    for months, count in counts.items():
        if f"{count}개 {months}개월" not in stats:
            fail("masters/programmes.html", f"hero stats missing '{count}개 {months}개월' (found {stats!r})")
    for removed_filter in ("degreeFilter", "durationFilter"):
        if finder.xpath(f'//*[@id="{removed_filter}"]'):
            fail("masters/programmes.html", f"removed filter unexpectedly present: {removed_filter}")
    for required_filter in ("groupFilter", "ieltsFilter", "backgroundFilter"):
        if not finder.xpath(f'//*[@id="{required_filter}"]'):
            fail("masters/programmes.html", f"required filter missing: {required_filter}")
    background_values = finder.xpath('//*[@id="backgroundFilter"]/option/@value')
    if background_values != ["", "open", "restricted"]:
        fail("masters/programmes.html", f"simplified background filter values incorrect: {background_values}")

# MRes cards must each lead to one of the nine programme detail pages.
mres_hub = parsed_pages.get(MASTERS_ROOT / "mres" / "index.html")
if mres_hub is not None:
    hrefs = mres_hub.xpath('//a[@href]/@href')
    for programme in MRES["programmes"]:
        if programme["detail_path"] not in hrefs:
            fail("masters/mres/index.html", f"MRes card missing link to {programme['detail_path']}")

# CSS url() references in masters stylesheets must resolve to real files.
for css in sorted(list(MASTERS_ROOT.rglob("*.css")) + [ROOT / "assets" / "guide.css"]):
    for ref in re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", css.read_text(encoding="utf-8")):
        if ref.startswith(("data:", "http:", "https:", "#")):
            continue
        target = local_target_from_url(ref) if ref.startswith("/") else (css.parent / ref).resolve()
        if not target.is_file():
            fail(css.relative_to(ROOT), f"missing CSS asset {ref}")

for value, locations in titles.items():
    if len(locations) > 1:
        fail("titles", f"duplicate title in {locations}: {value}")
for value, locations in descriptions.items():
    if len(locations) > 1:
        fail("descriptions", f"duplicate meta description in {locations}: {value}")
for value, locations in canonicals.items():
    if len(locations) > 1:
        fail("canonicals", f"duplicate canonical in {locations}: {value}")

og_asset = ROOT / EXPECTED_OG_IMAGE.lstrip("/")
if not og_asset.is_file():
    fail("assets", f"OG image file missing: {EXPECTED_OG_IMAGE}")

# Root social metadata belongs to the same preview PR as the masters pages.
root_doc = html.fromstring((ROOT / "index.html").read_text(encoding="utf-8"))
social_url = SITE_ORIGIN + "/assets/social/unnc-korea-share-20260909.jpg"
for prop, expected in (("og:image", social_url), ("og:image:secure_url", social_url),
                       ("og:image:width", "1200"), ("og:image:height", "630")):
    actual = root_doc.xpath(f'//meta[@property="{prop}"]/@content')
    if actual != [expected]:
        fail("index.html", f"root {prop} must be {expected!r}, got {actual}")
if root_doc.xpath('//meta[@name="twitter:card"]/@content') != ["summary_large_image"]:
    fail("index.html", "root Twitter large image card missing")
if not (ROOT / "assets/social/unnc-korea-share-20260909.jpg").is_file():
    fail("assets/social", "root social share image missing")

sitemap_path = ROOT / "sitemap.xml"
try:
    sitemap_raw = sitemap_path.read_text(encoding="utf-8")
    if "\\n" in sitemap_raw:
        fail("sitemap.xml", "literal \\n escape found; sitemap should use real line breaks")
    sitemap = ElementTree.parse(sitemap_path)
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    url_nodes = sitemap.findall("sm:url", namespace)
    sitemap_urls = [norm(node.findtext("sm:loc", default="", namespaces=namespace)) for node in url_nodes]
    if len(sitemap_urls) != len(set(sitemap_urls)):
        duplicates = [u for u, count in Counter(sitemap_urls).items() if count > 1]
        fail("sitemap.xml", f"duplicate URLs: {duplicates}")
    for node, url in zip(url_nodes, sitemap_urls):
        parsed = urlparse(url)
        if parsed.netloc != "unnc-korea.netlify.app":
            fail("sitemap.xml", f"unexpected sitemap host: {url}")
        target = local_target_from_url(parsed.path)
        if not target.exists():
            fail("sitemap.xml", f"URL has no local HTML target: {url}")
        lastmod = norm(node.findtext("sm:lastmod", default="", namespaces=namespace))
        if lastmod and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod):
            fail("sitemap.xml", f"invalid lastmod {lastmod!r} for {url}")
        elif lastmod:
            try:
                date.fromisoformat(lastmod)
            except ValueError:
                fail("sitemap.xml", f"impossible lastmod date {lastmod!r} for {url}")
    expected_masters_urls = {SITE_ORIGIN + public_path(page) for page in pages}
    actual_masters_urls = {u for u in sitemap_urls if urlparse(u).path.startswith("/masters")}
    missing = sorted(expected_masters_urls - actual_masters_urls)
    extra = sorted(actual_masters_urls - expected_masters_urls)
    if missing:
        fail("sitemap.xml", f"masters URLs missing: {missing}")
    if extra:
        fail("sitemap.xml", f"masters URLs without matching HTML: {extra}")
except Exception as exc:
    fail("sitemap.xml", f"XML parse/validation failed: {exc}")

robots_text = (ROOT / "robots.txt").read_text(encoding="utf-8")
expected_sitemap_line = f"Sitemap: {SITE_ORIGIN}/sitemap.xml"
if expected_sitemap_line not in robots_text:
    fail("robots.txt", f"missing {expected_sitemap_line}")

if warnings:
    print("WARNINGS")
    for item in warnings:
        print(f"- {item}")

if errors:
    print(f"FAILED: {len(errors)} issue(s)")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print("UNNC masters HTML QA passed")
print(f"HTML pages: {len(pages)}")
print(f"Taught detail pages: {len(taught_details)}")
print(f"MRes detail pages: {len(mres_details)}")
print(f"Unique titles/descriptions/canonicals: {len(titles)}/{len(descriptions)}/{len(canonicals)}")
print(f"Sitemap masters URLs: {len(actual_masters_urls)}")
print("Taught durations:", dict(sorted(Counter(c["duration_months"] for c in TAUGHT["courses"]).items())))
print("IELTS 6.0 group:", sum(c["english_profile"] == "lower_6_0" for c in TAUGHT["courses"]))
print("2027 intake pending:", sorted(c["name"] for c in TAUGHT["courses"] if c["intake_2027_status"].startswith("pending")))
