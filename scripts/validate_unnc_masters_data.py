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

long_courses = {c["name"] for c in courses if c["duration_months"] == 21}
assert long_courses == {"Computer Science", "Finance and Investment (Professional Accounting)"}

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
assert pending_intakes == {"Financial Technology", "Digital Screen Production"}

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

detail_paths = [c.get("detail_path") for c in courses if c.get("detail_path")]\nassert len(detail_paths) == 6, f"Expected 6 priority detail pages in data, got {len(detail_paths)}"\nassert len(set(detail_paths)) == 6, "Duplicate detail path"\nassert all(c.get("curriculum_2027_28_status") == "subject_to_change" for c in courses if c.get("detail_path"))\n\nprint("UNNC masters data validation passed")
print("programmes:", len(courses))
print("duration distribution:", durations)
print("IELTS 6.0 group:", len(lower))
print("2027 intake pending:", sorted(pending_intakes))
