#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = [ROOT / 'index.html', *ROOT.glob('unnc-*.html')]
replacements = {
    '공식 South Korea 기준과 영어조건을 분리해 확인합니다.': '한국 지원자 입학 기준과 영어조건을 분리해 확인합니다.',
    'UNNC는 한국 지원자에게 Preliminary Year(Year 1)과 Qualifying Year(Year 2)를 별도로 안내합니다.': '한국 지원자는 Preliminary Year(Year 1)과 Qualifying Year(Year 2) 기준을 구분해 적용합니다.',
    '한국 지원자 기준에서는 Preliminary Year의 대표 기준으로 Specialized High School Diploma 80% 또는 B 이상을 제시하고, Qualifying Year는 Foundation Programme 또는 대학 1년 이수를 요구합니다.': 'Preliminary Year의 대표 기준은 Specialized High School Diploma 80% 또는 B 이상이며, Qualifying Year는 Foundation Programme 또는 대학 1년 이수가 필요합니다.',
    '2027 최종 마감일은 아직 공식 공지 전입니다.': '2027 최종 마감일은 아직 발표되지 않았습니다.',
    '일반고·검정고시·기타 학력은 공식 페이지에 동일한 숫자 기준이 별도로 적혀 있지 않아 개별 확인이 필요': '일반고·검정고시·기타 학력은 동일한 숫자 기준이 별도로 공개되어 있지 않아 개별 확인이 필요',
    'TOEFL 수치는 UNNC 공식 가이드와 일부 최신 course prospectus 사이에 표시 차이가 있어, 이 페이지에서는 고정 수치로 단정하지 않고 지원 전공의 최신 prospectus를 최종 확인하도록 안내합니다.': 'TOEFL 기준은 지원 전공의 최신 prospectus를 기준으로 최종 확인합니다.',
    '2027 국제학생 일반 지원과 장학금의 최종 마감일이 게시되지 않았습니다.': '2027 국제학생 일반 지원과 장학금의 최종 마감일은 아직 발표되지 않았습니다.',
    '다만 현재 한국 지원자 기준이 숫자로 공개한 Preliminary Year 대표 기준은 Specialized High School Diploma 기준이므로 일반고 학력은 개별 확인이 필요합니다.': 'Preliminary Year에서 확인되는 대표 기준은 Specialized High School Diploma 기준이므로 일반고 학력은 개별 확인이 필요합니다.',
    'RMB · 공식 연간 총비용 추정': 'RMB · 연간 예상 총비용',
    '공식 페이지는 최대 4년까지 가능하다고 안내합니다.': '최대 4년까지 적용할 수 있습니다.',
    '2027 마감일은 아직 공식 발표 전이므로 동일 날짜를 미리 확정하지 않습니다.': '2027 마감일은 아직 발표되지 않았으며, 발표 전까지 2026 일정을 그대로 적용하지 않습니다.',
    'University of Nottingham의 UK·China·Malaysia 학생들이 같은 degree certificate를 받는다고 명시합니다.': 'University of Nottingham의 UK·China·Malaysia 학생들은 같은 degree certificate를 받습니다.',
    '영국·중국·말레이시아 캠퍼스에서 공부하는 University of Nottingham 학생이 같은 degree certificate를 받는다고 설명합니다.': '영국·중국·말레이시아 캠퍼스에서 공부하는 University of Nottingham 학생은 같은 degree certificate를 받습니다.',
    '세 캠퍼스 학생이 같은 degree certificate를 받는다는 것입니다.': '세 캠퍼스 학생은 같은 degree certificate를 받습니다.',
    '개별 증명서 표기나 학적 증명 세부는 지원·졸업 시점의 공식 문서를 확인하는 것이 가장 정확합니다.': '개별 증명서 표기와 학적 증명 세부사항은 지원·졸업 시점의 최신 규정을 적용합니다.',
    '같은 degree certificate, QS 순위, 4+0·2+2를 서로 섞지 않고 정확히 구분해 봅니다.': '같은 degree certificate, QS 순위, 4+0·2+2의 차이를 정확히 구분합니다.',
    '따라서 한국어 사이트에서도 ‘UNNC 세계 97위’처럼 별도 기관 순위로 오해될 표현보다 <strong>‘University of Nottingham · QS 세계 97위(2027)’</strong>라고 표시하는 것이 정확합니다.': '<strong>세계 97위는 UNNC 단독 순위가 아니라 University of Nottingham의 QS World University Rankings 2027 순위입니다.</strong>',
    '모든 degree programmes가 영어로 진행된다고 명시합니다.': '모든 degree programmes는 영어로 진행됩니다.',
    '다만 South Korea 국가별 공식 기준은 학교 유형과 지원 학년에 따라 다르므로 Preliminary Year와 Qualifying Year 기준을 구분해 확인해야 합니다.': '한국 지원자의 입학 기준은 학교 유형과 지원 학년에 따라 다르므로 Preliminary Year와 Qualifying Year 기준을 구분해 확인해야 합니다.',
}
for path in files:
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding='utf-8')
print('Visible institutional tone refinements applied')
