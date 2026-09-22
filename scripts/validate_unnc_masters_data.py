#!/usr/bin/env python3
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "unnc-masters-2027.json"
d = json.loads(DATA.read_text(encoding="utf-8"))
courses = d["courses"]

assert len(courses) == 26, f"Expected 26 full-time taught programmes, got {len(courses)}"
assert len({c["slug"] for c in courses}) == 26, "Duplicate programme slug"
assert all(c["study_mode"] == "Full time" for c in courses), "Non-full-time programme found"
assert not any("Business Administration" == c["name"] for c in courses), "Part-time MBA must not be in dataset"

durations = {}
for c in courses:
    durations[c["duration_months"]] = durations.get(c["duration_months"], 0) + 1
assert durations == {12: 24, 21: 2}, f"Unexpected duration distribution: {durations}"

assert {c["name"] for c in courses if c["duration_months"] == 21} == {
    "Computer Science",
    "Finance and Investment (Professional Accounting)",
}
assert not any(c["duration_months"] == 24 for c in courses)

lower = {c["name"] for c in courses if c["english_profile"] == "lower_6_0"}
assert lower == {
    "Computer Science",
    "Urbanism and Sustainable Environments",
    "Electronic Communications and Computer Engineering",
    "Innovative Design",
    "Intelligent Infrastructure and Management",
}

assert all(c["official_url"].startswith("https://www.nottingham.edu.cn/") for c in courses)
assert all(c["tuition"]["academic_year_2027_status"] == "pending" for c in courses)
assert all(c["tuition"]["total_programme_fee_2027_status"] == "pending_do_not_infer" for c in courses)

supply = next(c for c in courses if c["name"] == "International Business (Supply Chain Management)")
assert supply["tuition"]["amount_per_year"] == 150000
assert all(c["tuition"]["amount_per_year"] == 130000 for c in courses if c is not supply)

pending_intakes = {c["name"] for c in courses if c["intake_2027_status"].startswith("pending")}
assert pending_intakes == {
    "Financial Technology",
    "Digital Screen Production",
}

stale_start_dates = {
    c["name"]: c["start_date_official"]
    for c in courses
    if c["intake_2027_status"].startswith("pending")
}
assert stale_start_dates == {
    "Financial Technology": "September 2024",
    "Digital Screen Production": "September 2026",
}

gpa = d["global_requirements"]["south_korea_gpa"]["official_typical_minimums"]
assert gpa == [
    {"scale": 4.0, "values": [2.9, 3.3]},
    {"scale": 4.3, "values": [3.1, 3.5]},
    {"scale": 4.5, "values": [3.3, 3.7]},
]

confirmed = d["scholarships_2027"]["confirmed"]
assert {x["value"] for x in confirmed} == {"100% of first-year tuition", "50% of first-year tuition"}
assert {x["deadline"] for x in confirmed} == {"2027-05-31"}
assert d["application_2027"]["general_deadline_status"] == "pending"
assert d["tuition_and_costs"]["tuition_2027_status"] == "pending"

detail_paths = [c.get("detail_path") for c in courses if c.get("detail_path")]
assert len(detail_paths) == 26, f"Expected 26 taught detail pages in data, got {len(detail_paths)}"
assert len(set(detail_paths)) == 26, "Duplicate detail path"
assert all(c.get("curriculum_2027_28_status") == "subject_to_change" for c in courses if c.get("detail_path"))
assert all((DATA.parents[1] / p.lstrip("/")).is_file() for p in detail_paths), "Missing taught detail HTML"

innovative_design = next(c for c in courses if c["name"] == "Innovative Design")
assert innovative_design["additional_requirements"] == [
    "CV",
    "Portfolio demonstrating relevant design- or technology-related projects, practical experience and skills",
]
assert "requires both a CV and a portfolio" in innovative_design["current_official_entry_note"]

for required_interview_course in ("Applied Linguistics", "International Higher Education"):
    course = next(c for c in courses if c["name"] == required_interview_course)
    assert "Interview with course admissions tutor required" in course["additional_requirements"]

risky_link_terms = ("apply", "application portal", "how to apply")
assert not any(
    term in c["official_url"].lower()
    for c in courses
    for term in risky_link_terms
), "A programme official_url points to a direct application/how-to-apply page"

print("UNNC masters data validation passed")
print("programmes:", len(courses))
print("duration distribution:", durations)
print("IELTS 6.0 group:", len(lower))
print("2027 intake pending:", sorted(pending_intakes))
