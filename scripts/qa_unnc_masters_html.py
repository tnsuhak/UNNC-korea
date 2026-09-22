#!/usr/bin/env python3
"""Deterministic QA for the complete UNNC masters preview section."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
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
                if any(term in combined for term in ("application portal", "how to apply", "/apply", "apply now")):
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

    visible_text = norm(doc.text_content()).lower()
    if "자료 출처" in visible_text or "공식 확인 자료" in visible_text:
        fail(rel, "visible source box/label found")

    for asset in doc.xpath('//link[@href]/@href | //script[@src]/@src | //img[@src]/@src'):
        parsed = urlparse(asset)
        if parsed.scheme or asset.startswith("//") or asset.startswith("data:"):
            continue
        target = local_target_from_url(parsed.path) if parsed.path.startswith("/") else (page.parent / parsed.path).resolve()
        if not target.exists():
            fail(rel, f"missing local asset {asset}")

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

sitemap_path = ROOT / "sitemap.xml"
try:
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
