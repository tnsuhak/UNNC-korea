#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = [ROOT / 'index.html', *ROOT.glob('unnc-*.html')]
repls = {
    'UNNC 공식 안내에 따르면 ': '',
    'UNNC 공식 글로벌 리크루팅 안내는 ': '',
    'UNNC 공식 자료는 ': '',
    'UNNC 공식 홈페이지는 ': '',
    'UNNC 공식 설명의 핵심은 ': '',
    '현재 UNNC 공식 학비 페이지의 ': '',
    '현재 공식 학비 페이지의 ': '',
    '현재 공식 사이트에는 ': '',
    '현재 공식 페이지의 ': '',
    '현재 South Korea 공식 페이지는 ': '한국 지원자 기준에서는 ',
    'UNNC 공식 South Korea 페이지에 공개된 문구를 그대로 기준점으로 삼고': '한국 지원자 입학 기준을 적용하고',
    'South Korea 공식 페이지가 ': '한국 지원자 기준이 ',
    '공식 연간 예상 총비용': '연간 예상 총비용',
    '공식 예상 총비용': '예상 총비용',
    '공식 추정치': '예상비용',
    '현재 공식 기준': '현재 기준',
    '공식 수치': '2025 수치',
    '라고 명시합니다.': '입니다.',
    '라고 안내합니다.': '입니다.',
    '라고 설명합니다.': '입니다.',
}
for p in files:
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    for old, new in repls.items():
        text = text.replace(old, new)
    p.write_text(text, encoding='utf-8')
print('Direct authoritative tone quickfix applied')
