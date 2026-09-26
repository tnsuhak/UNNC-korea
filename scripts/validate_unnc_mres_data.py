#!/usr/bin/env python3
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "unnc-mres-2027.json"
d = json.loads(DATA.read_text(encoding="utf-8"))
courses = d["programmes"]

assert len(courses) == 9
assert len({c["slug"] for c in courses}) == 9
assert all(c["degree"] == "MRes" for c in courses)
assert all(c["study_mode"] == "Full time" for c in courses)
assert all(c["duration_months"] == 12 for c in courses)
assert all(c["start_dates"] == ["February", "September"] for c in courses)
assert all(c["english_profile"] == "IELTS 6.0 / each 5.5" for c in courses)
assert all(c["official_url"].startswith("https://www.nottingham.edu.cn/") for c in courses)
assert d["global_requirements"]["supervisor_contact_required_before_application"] is True
assert d["global_requirements"]["research_proposal"]["word_range"] == [1000, 3000]
assert d["intake_2027"]["february"]["application_deadline"] == "2026-10-31"
assert d["intake_2027"]["september"]["status"] == "pending"
assert d["tuition"]["academic_year_2027_status"] == "pending"
assert d["scholarships_2027"]["mres_specific_confirmed"] is False
assert "Postgraduate Taught" in d["scholarships_2027"]["note"]
detail_paths = [c.get("detail_path") for c in courses if c.get("detail_path")]
assert len(detail_paths) == 9
assert len(set(detail_paths)) == 9
assert all((DATA.parents[1] / p.lstrip("/")).is_file() for p in detail_paths), "Missing MRes detail HTML"
assert all(c.get("detail_status") == "published_in_preview" for c in courses)
print("UNNC MRes data validation passed")
