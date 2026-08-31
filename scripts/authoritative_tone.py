#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "index.html",
    ROOT / "unnc-admission-requirements-korea-2027.html",
    ROOT / "unnc-tuition-scholarships-2027.html",
    ROOT / "unnc-programmes-careers.html",
    ROOT / "unnc-nottingham-degree-uk-campus.html",
]

# Source verification belongs in the compact '자료 출처' section. Student-facing
# prose should state verified facts directly, like a university information site.
REPLACEMENTS = {
    "UNNC 공식 안내에 따르면 영국, 중국, 말레이시아 캠퍼스에서 공부하는 University of Nottingham 학생은 같은 degree certificate를 받습니다.":
        "영국과 중국 캠퍼스에서 공부하는 University of Nottingham 학생은 같은 degree certificate를 받습니다.",
    "현재 UNNC 공식 학비 페이지의 국제학생 학부 학비는 연 120,000 RMB입니다.":
        "국제학생 학부 학비는 연 120,000 RMB입니다.",
    "UNNC 공식 글로벌 리크루팅 안내는 모든 degree programmes가 영어로 진행된다고 명시합니다.":
        "모든 degree programmes는 영어로 진행됩니다.",
    "UNNC 공식 글로벌 리크루팅 안내는 UK, China, Malaysia 학생이 같은 degree certificate를 받는다고 명시합니다.":
        "UK와 China 캠퍼스의 학생은 같은 University of Nottingham degree certificate를 받습니다.",
    "UNNC 공식 글로벌 리크루팅 안내는 University of Nottingham의 UK·China·Malaysia 학생들이 같은 degree certificate를 받는다고 명시합니다.":
        "University of Nottingham의 UK·China 학생들은 같은 degree certificate를 받습니다.",
    "UNNC 공식 자료는 영국·중국·말레이시아 캠퍼스에서 공부하는 University of Nottingham 학생이 같은 degree certificate를 받는다고 설명합니다.":
        "영국·중국 캠퍼스의 University of Nottingham 학생은 같은 degree certificate를 받습니다.",
    "UNNC 공식 설명의 핵심은 세 캠퍼스 학생이 같은 degree certificate를 받는다는 것입니다.":
        "영국·중국 캠퍼스 학생은 같은 University of Nottingham degree certificate를 받습니다.",
    "UNNC 공식 홈페이지는 University of Nottingham이 QS World University Rankings 2027에서 세계 97위라고 안내합니다.":
        "University of Nottingham은 QS World University Rankings 2027에서 세계 97위입니다.",
    "현재 공식 학비 페이지의 국제학생 학부 학비는 연 120,000 RMB입니다.":
        "국제학생 학부 학비는 연 120,000 RMB입니다.",
    "현재 공식 기준 연 120,000 RMB입니다.":
        "연간 학비는 120,000 RMB입니다.",
    "캠퍼스 기숙사는 연 11,000~20,000 RMB이며, 학비·기숙사·보험·닝보 생활비를 포함한 공식 예상 총비용은 연 약 150,000~190,000 RMB입니다.":
        "캠퍼스 기숙사는 연 11,000~20,000 RMB이며, 학비·기숙사·보험·닝보 생활비를 포함한 연간 예상 총비용은 약 150,000~190,000 RMB입니다.",
    "학비, 기숙사, 의무보험, 닝보 생활비를 포함한 공식 추정치는 약 150,000~190,000 RMB입니다.":
        "학비, 기숙사, 의무보험, 닝보 생활비를 포함한 연간 예상비용은 약 150,000~190,000 RMB입니다.",
    "신입생은 원칙적으로 연간 학비를 전액 납부해야 하며, commencing students에는 일반적인 분납제가 제공되지 않는다고 공식 페이지가 안내합니다.":
        "신입생은 원칙적으로 연간 학비를 전액 납부하며, commencing students에게는 일반적인 분납제가 제공되지 않습니다.",
    "현재 공식 페이지의 2026 장학금 제출 마감은 5월 31일입니다.":
        "2026 장학금 제출 마감은 5월 31일입니다.",
    "현재 공식 페이지의 2026 장학금 마감은 5월 31일이며, 2027 마감일은 공식 발표 후 업데이트합니다.":
        "2026 장학금 마감은 5월 31일이었으며, 2027 마감일은 발표되는 대로 업데이트합니다.",
    "현재 UNNC가 공개한 South Korea 공식 기준을 바탕으로 정리했습니다.":
        "한국 지원자는 현재 입학 기준을 적용합니다.",
    "현재 South Korea 공식 페이지는 Preliminary Year의 대표 기준으로 Specialized High School Diploma 80% 또는 B 이상을 제시하고, Qualifying Year는 Foundation Programme 또는 대학 1년 이수를 요구합니다.":
        "한국 지원자의 Preliminary Year 대표 기준은 Specialized High School Diploma 80% 또는 B 이상이며, Qualifying Year는 Foundation Programme 또는 대학 1년 이수를 요구합니다.",
    "UNNC 공식 South Korea 페이지에 공개된 문구를 그대로 기준점으로 삼고, 그 밖의 학력은 임의의 한국 내신 등급으로 환산하지 않습니다.":
        "한국 지원자 입학 기준을 적용하며, 그 밖의 학력은 임의의 한국 내신 등급으로 환산하지 않습니다.",
    "현재 South Korea 공식 페이지가 숫자로 공개한 Preliminary Year 대표 기준은 Specialized High School Diploma 기준이므로 일반고 학력은 개별 확인이 필요합니다.":
        "Preliminary Year의 대표 기준은 Specialized High School Diploma 기준이므로 일반고 학력은 개별 확인이 필요합니다.",
    "현재 공식 사이트에는 2027 국제학생 일반 지원과 장학금의 최종 마감일이 게시되지 않았습니다.":
        "2027 국제학생 일반 지원과 장학금의 최종 마감일은 아직 발표되지 않았습니다.",
    "현재 공식 사이트에는 2027 국제학생 지원·장학금 최종 마감일이 아직 게시되지 않았습니다.":
        "2027 국제학생 지원·장학금 최종 마감일은 아직 발표되지 않았습니다.",
    "UNNC 공식 최소조건으로 ‘내신 3~4등급’이 공개돼 있지 않으므로 공식 컷처럼 안내하지 않습니다.":
        "‘내신 3~4등급’을 입학 최소조건으로 사용하지 않습니다. 한국 학력은 학교 유형과 지원 학년에 맞춰 확인합니다.",
    "2024/25 Careers Report에 따르면 2025 학부 졸업생 가운데":
        "2025 학부 졸업생 가운데",
    "UNNC는 <span class=\"hi\">QS Stars 5-star institution</span>으로도 소개됩니다.":
        "UNNC는 <span class=\"hi\">QS Stars 5-star institution</span>입니다.",
    "현재 국제학생 학부 공식 학비.":
        "국제학생 학부 학비.",
    "아래는 현재 한국 지원자 입학 기준을 바탕으로 정리했습니다.":
        "한국 지원자는 아래 입학 기준을 적용합니다.",
    "<span class=\"hl\">South Korea 공식 대표 기준</span>":
        "<span class=\"hl\">한국 고교 학력</span>",
    "기존의 ‘내신 3~4등급’ 같은 비공식 컷은 공식 최소조건으로 사용하지 않습니다. 학교 유형과 학력에 따라 South Korea 기준을 적용해 확인합니다.":
        "‘내신 3~4등급’을 고정 입학조건으로 적용하지 않습니다. 학교 유형과 학력에 따라 지원 학년을 확인합니다.",
    "공식 발표 전에는 임의의 날짜를 확정해서 안내하지 않습니다.":
        "2027 일정이 발표되기 전에는 임의의 날짜를 확정하지 않습니다.",
    "<title>UNNC 학비·장학금 2027 | 오늘 환율·기숙사·생활비 | TNS유학</title>":
        "<title>UNNC 학비·장학금 | 기숙사·생활비·2027 준비 | TNS유학</title>",
    "<meta property=\"og:title\" content=\"UNNC 학비·장학금 2027 | 오늘 환율·기숙사·생활비 | TNS유학\">":
        "<meta property=\"og:title\" content=\"UNNC 학비·장학금 | 기숙사·생활비·2027 준비 | TNS유학\">",
    "\"headline\":\"UNNC 학비·장학금 오늘 환율로 계산\"":
        "\"headline\":\"UNNC 학비·장학금과 연간 비용\"",
    "<h1>UNNC 학비·장학금<br>오늘 환율로 계산</h1>":
        "<h1>UNNC 학비·장학금<br>연간 비용 정리</h1>",
    "<b>약 3,054만원~</b><span>연간 총비용 시작</span>":
        "<b>약 3,054만원부터</b><span>연간 예상 총비용</span>",
    "약 3,054만원~약 3,869만원":
        "약 3,054만~3,869만원",
    "공식 수치": "2025 수치",
    "현재 공식 기준": "현재 기준",
    "공식 연간 예상 총비용": "연간 예상 총비용",
}

BANNED = [
    "공식 안내에 따르면",
    "공식 자료에 따르면",
    "공식 페이지에 따르면",
    "공식 홈페이지에 따르면",
    "모집자료에 따르면",
    "브로셔에 따르면",
    "공식 자료는",
    "공식 설명의 핵심",
    "Careers Report에 따르면",
    "South Korea 공식 대표 기준",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    if args.fix:
        for path in FILES:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            for old, new in REPLACEMENTS.items():
                text = text.replace(old, new)
            path.write_text(text, encoding="utf-8")

    problems: list[str] = []
    for path in FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in BANNED:
            if phrase in text:
                problems.append(f"{path.name}: avoid source-attribution wording: {phrase}")

    if problems:
        print("\n".join(problems))
        return 1
    print("Authoritative Korean tone check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
