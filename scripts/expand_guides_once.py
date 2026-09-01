#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://unnc-korea.netlify.app"
UPDATED = "2026-09-02"

NAV = '''<div class="top">UNNC 한국어 입학 안내 · TNS유학</div>
<nav class="nav"><a class="brand" href="/">UNNC <span>Korea</span></a><div class="navlinks"><a href="/">학교소개</a><a href="unnc-admission-requirements-korea-2027.html">입학조건</a><a href="unnc-tuition-scholarships-2027.html">학비·장학금</a><a href="unnc-programmes-careers.html">전공·진로</a><a href="unnc-nottingham-degree-uk-campus.html">학위·영국연계</a><a href="#contact">상담</a></div></nav>'''
CTA = '''<section class="cta" id="contact"><div class="wrap"><h2>UNNC 지원, 한국학생 기준으로 확인하세요</h2><p>학력·희망 전공·영어성적과 예산을 기준으로 지원 전략을 함께 점검해 드립니다.</p><a class="btn" href="http://pf.kakao.com/_xfXsxjE" target="_blank" rel="noopener">카카오톡 상담</a><a class="btn alt" href="tel:0232881733">02-3288-1733</a></div></section>
<footer><div class="wrap">㈜티앤에스월드와이드 · 대표 신윤옥 · 사업자등록번호 220-87-54964<br>서울 강남구 테헤란로 5길 7 KG타워 B1 · 02-3288-1733 · tns@tnsuhak.com</div></footer>'''


def article_schema(title, description, slug):
    return json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":description,"dateModified":UPDATED,"mainEntityOfPage":f"{BASE}/{slug}","publisher":{"@type":"Organization","name":"TNS유학 ㈜티앤에스월드와이드"}}, ensure_ascii=False, separators=(",", ":"))


def faq_schema(faqs):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}, ensure_ascii=False, separators=(",", ":"))


def related(*items):
    cards = "".join(f'<article class="card"><h3><a href="{href}">{title}</a></h3><p>{desc}</p></article>' for href,title,desc in items)
    return f'<section class="section"><h2>함께 보면 좋은 UNNC 가이드</h2><div class="grid">{cards}</div></section>'


def make_page(slug, title, description, eyebrow, h1, intro, hero, quick, body, faqs, sources):
    qhtml = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b,s in quick)
    faqhtml = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
    sourcehtml = "<br>".join(f'<a href="{url}" target="_blank" rel="noopener">{label}</a>' for label,url in sources)
    html = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{description}"><meta name="robots" content="index, follow"><link rel="canonical" href="{BASE}/{slug}">
<meta property="og:type" content="article"><meta property="og:site_name" content="UNNC Korea | TNS유학"><meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="{BASE}/{slug}"><meta property="og:locale" content="ko_KR"><meta name="twitter:card" content="summary">
<script type="application/ld+json">{article_schema(h1.replace('<br>',' '), description, slug)}</script><script type="application/ld+json">{faq_schema(faqs)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/guide.css"></head><body>
{NAV}
<header class="hero" style="--hero-image:url('{hero}')"><div class="wrap"><div class="crumb"><a href="/">홈</a> › {eyebrow}</div><div class="eyebrow">{eyebrow}</div><h1>{h1}</h1><p>{intro}</p></div></header>
<div class="wrap quick">{qhtml}</div><main class="wrap">{body}<section class="section faq"><h2>자주 묻는 질문</h2>{faqhtml}</section><section class="section sources"><strong>자료 출처</strong><br>{sourcehtml}</section></main>{CTA}</body></html>'''
    (ROOT / slug).write_text(html, encoding="utf-8")


P_GUIDE = "https://20anniversary.nottingham.edu.cn/documents/Student-Recruitment/International-student-guide-2026.pdf"

make_page(
    "unnc-application-documents-2027.html",
    "UNNC 지원서류·지원준비 2027 | 추천서·PS·성적표 | TNS유학",
    "UNNC 2027 지원 준비에 필요한 성적표, 졸업증명, 추천서, Personal Statement, 여권, 영어성적과 증명사진을 체크리스트로 정리했습니다.",
    "APPLICATION DOCUMENTS",
    "UNNC 지원서류와<br>2027 지원 준비",
    "입학조건을 확인한 다음에는 실제 지원에 필요한 서류를 빠짐없이 준비해야 합니다. 한국학생이 미리 준비할 서류와 2027 일정 확인 포인트를 정리했습니다.",
    "assets/embedded/886d437bcaf03f35.webp",
    [("추천서 1부","학교 레터헤드·서명/직인"),("Personal Statement","지원동기·학업계획"),("여권 사본","주요면 준비"),("2027 일정","발표 후 확정")],
    '''<section class="section"><h2>지원서류는 이렇게 준비합니다</h2><p class="lead">학업서류, 지원동기, 신분증빙, 영어성적을 한 번에 준비하면 지원 과정이 훨씬 수월합니다.</p><div class="grid"><article class="card"><span class="tag">ACADEMIC</span><h3>학업 관련 서류</h3><ul><li>학교 성적표: 졸업 전이라면 현재까지의 성적</li><li>고등학교 졸업증명서</li><li>대학원 지원자는 대학 성적표와 학위증명</li><li>학교 레터헤드에 작성되고 서명 또는 직인이 포함된 추천서 1부</li></ul></article><article class="card"><span class="tag">PERSONAL</span><h3>지원자 관련 서류</h3><ul><li>Personal Statement</li><li>여권 주요면 사본</li><li>IELTS·PTE 등 영어성적표(이미 취득한 경우)</li><li>흰색 배경 증명사진</li></ul></article></div></section>
<section class="section"><h2>증명사진 규격</h2><div class="notice">2×2 inch 컬러 사진, 흰색 배경, 머리가 사진 크기의 약 3분의 2를 차지하도록 준비합니다. 파일은 JPG, 4:3 비율, 최소 320×240 pixels, 100~500KB 규격이 안내되어 있습니다.</div></section>
<section class="section"><h2>2027 지원 일정은 과거 날짜와 구분합니다</h2><div class="grid"><article class="card"><h3>2026 일반 지원</h3><p>2026 국제학생 일반 지원 마감은 6월 30일이었습니다.</p></article><article class="card"><h3>2026 장학금</h3><p>Nottingham Global 장학금의 2026 제출 마감은 5월 31일이었습니다.</p></article></div><p class="lead">2027 일반 지원과 장학금의 최종 일정은 아직 발표되지 않았습니다. 2026 날짜를 2027 일정으로 그대로 적용하지 않습니다.</p></section>
<section class="section"><h2>한국학생 준비 순서</h2><div class="table-wrap"><table><thead><tr><th>순서</th><th>준비 내용</th><th>확인할 점</th></tr></thead><tbody><tr><td>1</td><td>지원 학년 결정</td><td>Preliminary Year / Qualifying Year 구분</td></tr><tr><td>2</td><td>전공 결정</td><td>Maths·Physics 등 선수과목 확인</td></tr><tr><td>3</td><td>학업서류 준비</td><td>성적표·졸업/재학증명</td></tr><tr><td>4</td><td>추천서·PS 준비</td><td>지원동기와 학업계획을 일관되게 구성</td></tr><tr><td>5</td><td>영어성적 준비</td><td>지원 학년·전공별 IELTS/PTE 조건 확인</td></tr></tbody></table></div></section>'''+related(("unnc-admission-requirements-korea-2027.html","UNNC 2027 한국학생 입학조건","Year 1·Year 2와 영어조건을 먼저 확인합니다."),("unnc-tuition-scholarships-2027.html","학비·장학금","지원 전 전체 예산과 장학금 구조를 확인합니다.")),
    [("UNNC 지원서류는 무엇이 필요한가요?","학교 성적표와 졸업증명, 추천서 1부, Personal Statement, 여권 사본, 영어성적(보유 시), 증명사진 등을 준비합니다."),("추천서는 몇 부가 필요한가요?","2026 국제학생 가이드에는 학교 레터헤드에 작성되고 서명 또는 직인이 포함된 추천서 1부가 안내되어 있습니다."),("2027 지원 마감은 언제인가요?","2027 국제학생 일반 지원과 장학금의 최종 마감일은 아직 발표되지 않았습니다.")],
    [("UNNC · South Korea undergraduate entry requirements","https://www.nottingham.edu.cn/en/Study-with-us/Undergraduate/Entry-requirements/International-applicants.aspx?country=South+Korea&level=Undergraduate"),("UNNC · International Student Guide 2026",P_GUIDE)]
)

make_page(
    "unnc-accommodation-campus-life.html",
    "UNNC 기숙사·캠퍼스 생활 | 1인실 비용·시설 | TNS유학",
    "UNNC 국제학생 기숙사 보장, 11동·12B동·20동 비용과 방 구조, 인터넷·청소·보안·의료·캠퍼스 생활시설을 정리했습니다.",
    "ACCOMMODATION & CAMPUS LIFE",
    "UNNC 기숙사와<br>캠퍼스 생활",
    "국제학생 기숙사 비용과 방 형태, 캠퍼스 안에서 생활할 때 필요한 보안·의료·생활편의 시설까지 한 번에 확인합니다.",
    "assets/embedded/2e63f5142d96ea81.webp",
    [("11,000~20,000 RMB","연간 기숙사비"),("1인실 선택","11동·12B동"),("도보 약 5분","메인 강의동"),("24시간","보안·의료 지원")],
    '''<section class="section"><h2>국제학생 기숙사</h2><p class="lead">입학을 수락한 국제학생에게는 기숙사 방이 보장됩니다. 모든 객실은 가구와 인터넷 사용 환경을 갖추고 있습니다.</p><div class="table-wrap"><table><thead><tr><th>기숙사</th><th>연간 비용</th><th>형태</th><th>주요 특징</th></tr></thead><tbody><tr><td>Residence Building 11</td><td>20,000 RMB</td><td>1인실</td><td>개인 화장실·샤워실, 메인 강의동 도보 약 5분</td></tr><tr><td>Residence Building 12B</td><td>16,000 RMB</td><td>1인실</td><td>개인 화장실·샤워실, 메인 강의동 도보 약 5분</td></tr><tr><td>Residence Building 20</td><td>11,000 RMB</td><td>4-bedroom flat</td><td>개인 침실 + 공용 거실·샤워실·화장실</td></tr></tbody></table></div></section>
<section class="section"><h2>방 안에는 무엇이 있나요?</h2><div class="grid3"><article class="card"><h3>침실</h3><p>에어컨, 침대, 책상, 의자, 옷장, 매트리스 등 기본 가구가 제공됩니다. 20동은 책장도 포함됩니다.</p></article><article class="card"><h3>주방·세탁</h3><p>11동과 12B동은 공용 주방과 세탁실을 사용합니다. 주방에는 냉장고, 전자레인지, 인덕션, 전기오븐 등이 마련되어 있습니다.</p></article><article class="card"><h3>인터넷·청소</h3><p>무료 인터넷이 제공되며 객실 청소 서비스는 월 2회 포함됩니다.</p></article></div></section>
<section class="section"><h2>생활 지원과 안전</h2><div class="grid"><article class="card"><h3>24시간 보안</h3><p>기숙사에는 warden, deputy warden, tutors가 생활을 지원하고 24시간 보안 체계가 운영됩니다.</p></article><article class="card"><h3>24시간 의료 지원</h3><p>캠퍼스 클리닉의 의사와 간호사가 24시간 on-call로 운영되며, 인근에는 응급실을 갖춘 사립병원도 있습니다.</p></article></div></section>
<section class="section"><h2>캠퍼스 생활편의</h2><p class="lead">캠퍼스의 UK-style high street에는 학생들이 일상적으로 이용할 수 있는 생활시설이 모여 있습니다.</p><div class="grid"><article class="card"><h3>교내 편의시설</h3><p>cinema bookstore, 우체국, 드라이클리닝, 슈퍼마켓, 미용실, ATM, 여러 식당 등이 운영됩니다.</p></article><article class="card"><h3>학생 지원</h3><p>The Hub, Residential College, Student Engagement Office와 Department of Campus Life가 wellbeing, 학생활동, 행정·생활 지원을 제공합니다.</p></article></div></section>'''+related(("unnc-tuition-scholarships-2027.html","UNNC 학비·장학금","기숙사를 포함한 연간 예상 총비용을 같이 계산합니다."),("unnc-ningbo-china-life.html","닝보 유학생활","캠퍼스 밖 닝보 생활환경과 상하이 접근성을 확인합니다.")),
    [("국제학생은 기숙사가 보장되나요?","입학을 수락한 국제학생에게는 UNNC 기숙사 방이 보장됩니다."),("UNNC 기숙사비는 얼마인가요?","2026 국제학생 안내의 대표 기숙사는 연 11,000~20,000 RMB입니다."),("1인실이 있나요?","11동과 12B동은 개인 화장실과 샤워실이 있는 1인실입니다.")],
    [("UNNC · Accommodation","https://www.nottingham.edu.cn/en/accommodation"),("UNNC · International Student Guide 2026",P_GUIDE)]
)

make_page(
    "unnc-exchange-study-abroad.html",
    "UNNC 교환학생·Study Abroad | 해외교환·Summer School | TNS유학",
    "UNNC 교환학생, Study Abroad, Summer School의 차이와 학비 구조, 한 학기·1년 파트너 대학 교환 기회를 정리했습니다.",
    "EXCHANGE & STUDY ABROAD",
    "UNNC 교환학생과<br>Study Abroad",
    "UNNC 재학 중 해외 대학에서 공부하는 방법은 Exchange, Study Abroad, Summer School로 나눠 볼 수 있습니다. 비용과 기간이 서로 다릅니다.",
    "assets/embedded/fb37d028ec91561a.webp",
    [("160+","글로벌 파트너"),("40+","국가·지역"),("1학기 / 1년","Exchange"),("추가 수업료 없음","일반 Exchange")],
    '''<section class="section"><h2>세 가지 해외 학업 방식</h2><div class="grid3"><article class="card"><span class="tag">EXCHANGE</span><h3>교환학생</h3><p>학부생이 파트너 대학에서 한 학기 또는 한 학년을 공부합니다. 학점은 Nottingham degree 과정에 반영됩니다.</p></article><article class="card"><span class="tag">STUDY ABROAD</span><h3>Study Abroad</h3><p>영국 캠퍼스 또는 승인된 파트너 대학에서 공부할 수 있으며 추가 비용이 발생할 수 있습니다.</p></article><article class="card"><span class="tag">SUMMER SCHOOL</span><h3>Summer School</h3><p>정규 학기에서 빠지지 않고 여름방학 동안 해외 학업 경험을 쌓는 방식입니다.</p></article></div></section>
<section class="section"><h2>Exchange 학비 구조</h2><div class="answer"><strong>핵심:</strong> 일반적인 Exchange에서는 UNNC 학비를 계속 납부하고 교환 파트너 대학에는 별도 수업료를 내지 않습니다.</div><p class="lead">항공료, 기숙사, 보험, 비자, 현지 생활비 등은 별도로 고려해야 합니다.</p></section>
<section class="section"><h2>Exchange와 2+2는 다릅니다</h2><div class="table-wrap"><table><thead><tr><th>구분</th><th>기간</th><th>학비</th><th>학위 구조</th></tr></thead><tbody><tr><td>Exchange</td><td>보통 1학기 또는 1년</td><td>UNNC 학비 납부, 파트너 대학 수업료 없음</td><td>UNNC/Nottingham 학위과정의 일부</td></tr><tr><td>Study Abroad</td><td>프로그램별</td><td>추가 비용 가능</td><td>취득 학점을 최종 학위에 반영</td></tr><tr><td>2+2</td><td>일부 전공 후반 2년</td><td>영국 기간은 UK international fee</td><td>전공 자체의 학업 구조</td></tr></tbody></table></div></section>
<section class="section"><h2>어떤 학생에게 잘 맞나요?</h2><div class="grid"><article class="card"><h3>글로벌 경험을 넓히고 싶은 학생</h3><p>전공을 유지하면서 다른 국가의 대학 환경을 경험하고 싶은 경우 Exchange가 잘 맞습니다.</p></article><article class="card"><h3>영국 캠퍼스 경험이 중요한 학생</h3><p>장기간 영국에서 공부하고 싶다면 전공별 2+2 가능 여부와 Study Abroad 선택지를 함께 비교하는 것이 좋습니다.</p></article></div></section>'''+related(("unnc-nottingham-degree-uk-campus.html","노팅엄 학위·2+2","Exchange와 2+2의 차이를 학위 구조와 함께 봅니다."),("unnc-tuition-scholarships-2027.html","학비·장학금","해외 이동 시 전체 예산 차이를 확인합니다.")),
    [("UNNC 교환학생은 얼마나 갈 수 있나요?","Exchange는 일반적으로 한 학기 또는 한 학년 동안 파트너 대학에서 공부하는 방식입니다."),("교환 대학에 수업료를 또 내나요?","일반적인 Exchange에서는 UNNC 학비를 계속 납부하고 파트너 대학에는 별도 수업료를 내지 않습니다."),("2+2와 교환학생은 같은가요?","아닙니다. 2+2는 일부 전공의 학업 구조이고 Exchange는 정규 학위과정 중 일정 기간 파트너 대학에서 공부하는 방식입니다.")],
    [("UNNC · Global opportunities","https://www.nottingham.edu.cn/en/global"),("UNNC · International Student Guide 2026",P_GUIDE)]
)

make_page(
    "unnc-how-study-english-teaching.html",
    "UNNC 영어수업·수업방식 | 세미나·모듈·학업지원 | TNS유학",
    "UNNC의 영어 수업, 15~20명 세미나, 강의·그룹워크·발표·실험, Personal Tutor와 도서관 학업지원, 학사일정을 정리했습니다.",
    "HOW WILL I STUDY",
    "UNNC 수업은<br>어떻게 진행되나요?",
    "모든 학위과정은 영어로 운영됩니다. 대형 강의와 소규모 세미나, 과제·시험, 그룹워크와 발표를 함께 경험하는 영국식 학습 구조입니다.",
    "assets/embedded/6702ac55ed7d1baf.webp",
    [("100% 영어","degree programmes"),("15~20명","소규모 세미나"),("12주 × 2","정규 teaching blocks"),("Personal Tutor","개별 학업 지원")],
    '''<section class="section"><h2>강의만 듣는 방식이 아닙니다</h2><div class="grid"><article class="card"><h3>Lecture + Seminar</h3><p>큰 강의 그룹과 약 15~20명 규모의 소규모 seminar를 함께 운영합니다. 세미나에서는 토론과 상호작용 비중이 높습니다.</p></article><article class="card"><h3>Group work + Presentation</h3><p>수업 밖 독립학습, 그룹 프로젝트, 발표를 수행하며 전공에 따라 field work와 laboratory work도 포함됩니다.</p></article></div></section>
<section class="section"><h2>Module 중심 학사 구조</h2><p class="lead">학사·석사 과정은 module 단위로 구성되며 매 학기 필수와 선택 module을 조합합니다. 평가는 전공과 module에 따라 coursework, exam 또는 두 방식을 함께 사용합니다.</p><div class="notice">독립적으로 자료를 읽고 스스로 학습을 구조화하는 능력, 협업, 논리적 사고와 비판적 성찰을 중요하게 다룹니다.</div></section>
<section class="section"><h2>학업 지원</h2><div class="grid3"><article class="card"><h3>Academic consultation</h3><p>교수진과 개별 상담을 통해 과제와 학업 진행 상황을 논의할 수 있습니다.</p></article><article class="card"><h3>Personal Tutor</h3><p>개인 tutor가 배정되어 학업 과정 전반을 지원합니다.</p></article><article class="card"><h3>Library</h3><p>100만 권 이상의 인쇄·디지털 도서와 저널, 그룹스터디 공간, 조용한 학습공간, PC·노트북 등 다양한 학습자원을 이용할 수 있습니다.</p></article></div></section>
<section class="section"><h2>학사일정</h2><div class="table-wrap"><table><thead><tr><th>구분</th><th>일정</th></tr></thead><tbody><tr><td>Academic year</td><td>9월 초 시작 → 다음 해 6월 중순 종료</td></tr><tr><td>Semester</td><td>2개 학기</td></tr><tr><td>Teaching block</td><td>각 학기 12주 수업 후 시험기간</td></tr><tr><td>Winter vacation</td><td>1월 말 또는 2월 초부터 약 4주</td></tr><tr><td>Summer vacation</td><td>6월 중순부터 8월 말</td></tr></tbody></table></div></section>'''+related(("unnc-programmes-careers.html","UNNC 전공·졸업 후 진로","전공별 학업 방향과 졸업 후 선택지를 함께 확인합니다."),("unnc-exchange-study-abroad.html","교환학생·Study Abroad","재학 중 해외 학업 경험을 확장하는 방법을 확인합니다.")),
    [("UNNC 수업은 모두 영어인가요?","모든 degree programmes는 영어로 진행됩니다."),("세미나 수업은 몇 명 정도인가요?","일반적으로 소규모 세미나는 약 15~20명 규모로 운영됩니다."),("학업 상담을 받을 수 있나요?","Academic staff와 개별 consultation이 가능하고 Personal Tutor가 배정됩니다.")],
    [("UNNC · International Student Guide 2026",P_GUIDE)]
)

make_page(
    "unnc-ningbo-china-life.html",
    "UNNC 닝보 유학생활 | 상하이 2시간·중국생활 | TNS유학",
    "UNNC가 위치한 닝보의 상하이 접근성, 교통, 생활환경, 음식, 캠퍼스 편의시설과 중국에서 공부하는 장점을 한국학생 관점에서 정리했습니다.",
    "LIFE IN NINGBO",
    "UNNC가 있는 닝보,<br>어떤 도시인가요?",
    "닝보는 저장성 항저우만 남쪽에 위치한 국제 항구도시입니다. 상하이에서 약 2시간 거리이며 중국 생활과 영국식 대학 교육을 함께 경험할 수 있습니다.",
    "assets/embedded/fb37d028ec91561a.webp",
    [("약 2시간","상하이 접근"),("970만+","닝보 인구"),("국제 항구도시","Zhejiang"),("다양한 음식","한국·일본·서양식")],
    '''<section class="section"><h2>상하이와 가까운 저장성 국제도시</h2><p class="lead">닝보는 항저우만 남쪽에 있으며 상하이에서 약 2시간 거리입니다. 버스·기차·항공 교통망을 이용해 중국 주요 도시와 아시아 다른 지역으로 이동하기 좋습니다.</p><div class="grid"><article class="card"><h3>도시 규모</h3><p>인구 970만 명 이상, urban area 약 3,730㎢ 규모의 대도시입니다.</p></article><article class="card"><h3>국제 비즈니스 환경</h3><p>오랜 항구도시이자 제조·물류·무역 활동이 활발한 지역으로 중국 경제와 산업을 가까이에서 경험할 수 있습니다.</p></article></div></section>
<section class="section"><h2>먹거리와 생활</h2><div class="grid3"><article class="card"><h3>다양한 음식</h3><p>중국 음식뿐 아니라 인도, 이탈리아, 레바논, 터키, 일본, 한국, 태국, 멕시코 등 다양한 국제 음식점이 있습니다.</p></article><article class="card"><h3>캠퍼스 내 식음료</h3><p>중국식 식당과 함께 Starbucks, 일본·한국 음식 등 여러 선택지가 있습니다.</p></article><article class="card"><h3>온라인 생활</h3><p>중국의 발달한 온라인 쇼핑 환경을 이용해 수입식품과 생활용품을 비교적 쉽게 구할 수 있습니다.</p></article></div></section>
<section class="section"><h2>중국에서 공부하는 의미</h2><div class="answer"><strong>핵심:</strong> 영어로 University of Nottingham 학위과정을 공부하면서 중국어와 중국의 산업·비즈니스 환경을 일상 속에서 함께 경험할 수 있습니다.</div><p class="lead">향후 중국·아시아 비즈니스, 글로벌 기업, 대학원 진학을 고려하는 학생에게는 학업 외의 지역 경험도 중요한 자산이 될 수 있습니다.</p></section>
<section class="section"><h2>캠퍼스와 도시 생활을 연결해서 봅니다</h2><div class="grid"><article class="card"><h3>캠퍼스 안</h3><p>기숙사, 식당, 슈퍼마켓, 우체국, ATM, 학생지원시설 등이 모여 있습니다.</p></article><article class="card"><h3>캠퍼스 밖</h3><p>쇼핑몰과 엔터테인먼트 시설도 도보 또는 짧은 버스·택시 이동 범위에 있습니다.</p></article></div></section>'''+related(("unnc-accommodation-campus-life.html","기숙사·캠퍼스 생활","실제 거주 비용과 방 구조, 안전·의료 지원을 확인합니다."),("unnc-nottingham-degree-uk-campus.html","노팅엄 학위·영국연계","중국에서 공부하면서 받는 학위와 2+2 구조를 확인합니다.")),
    [("UNNC는 상하이에서 먼가요?","닝보는 상하이에서 약 2시간 거리입니다."),("닝보에서 한국 음식을 구하기 어렵나요?","닝보에는 한국을 포함한 다양한 국제 음식점이 있고 캠퍼스에도 여러 종류의 식음료 옵션이 있습니다."),("중국어를 못해도 UNNC 수업을 들을 수 있나요?","학위과정은 영어로 운영됩니다. 중국어는 생활과 현지 경험을 넓히는 추가 강점이 될 수 있습니다.")],
    [("UNNC · Life in Ningbo","https://www.nottingham.edu.cn/en/university-life/life-in-ningbo.aspx"),("UNNC · International Student Guide 2026",P_GUIDE)]
)

make_page(
    "unnc-career-support-further-study.html",
    "UNNC 취업·대학원 진학 지원 | 인턴십·1:1 커리어 상담 | TNS유학",
    "UNNC Career and Employability Service의 인턴십, International Career Week, 70명+ 커리어 adviser, 90개+ 워크숍, 대학원 진학 상담을 정리했습니다.",
    "CAREER & FURTHER STUDY SUPPORT",
    "UNNC 취업·대학원<br>진학 지원",
    "졸업 결과만 보는 것보다 재학 중 어떤 커리어·대학원 진학 지원을 받을 수 있는지 함께 보는 것이 중요합니다.",
    "assets/embedded/0cddcf1b60ebd2e7.webp",
    [("70+","Career advisers"),("90+","Career skill workshops"),("40+","Nottingham Advantage modules"),("1:1","Career·Further study 상담")],
    '''<section class="section"><h2>취업 준비 지원</h2><div class="grid3"><article class="card"><h3>Campus Recruitment</h3><p>Employer Presentation과 교내 채용 활동을 통해 기업과 학생을 연결합니다.</p></article><article class="card"><h3>Summer Placement</h3><p>기업과 협력해 여름 인턴십·placement 기회를 제공하고 실제 업무환경 경험을 지원합니다.</p></article><article class="card"><h3>International Career Week</h3><p>International Student Job Fair, Career Forum, 비자 정책 안내 등을 통해 국제학생의 중국 취업 이해를 돕습니다.</p></article></div></section>
<section class="section"><h2>개인별 커리어 지원</h2><div class="grid"><article class="card"><h3>70명+ Career Advisers</h3><p>커리어 staff, industry experts, headhunters, further study consultants, alumni로 구성된 adviser pool을 통해 1-to-1 career advice를 받을 수 있습니다.</p></article><article class="card"><h3>90개+ Skills Workshops</h3><p>리더십, 커뮤니케이션, 전략적 사고 등 취업역량을 높이는 interactive workshop이 운영됩니다.</p></article></div><div class="grid" style="margin-top:18px"><article class="card"><h3>AI Career Lab</h3><p>AI 기반 CV와 interview guidance 및 feedback을 제공하는 커리어 지원 도구가 운영됩니다.</p></article><article class="card"><h3>Nottingham Advantage Award</h3><p>세 캠퍼스 학습 플랫폼에서 40개 이상의 module을 통해 학업 외 역량과 employability를 확장할 수 있습니다.</p></article></div></section>
<section class="section"><h2>대학원 진학 지원</h2><div class="grid3"><article class="card"><h3>Further Study Fair</h3><p>대학원 관계자와 직접 만나 프로그램과 입학정보를 확인할 수 있습니다.</p></article><article class="card"><h3>GRE·GMAT Practice</h3><p>실제 시험 환경을 가정한 practice test를 통해 시험 준비를 지원합니다.</p></article><article class="card"><h3>Individual Advising</h3><p>대학원 진학 counsellor와 1:1 상담을 통해 학교 선택, 지원전략과 application preparation을 점검할 수 있습니다.</p></article></div></section>
<section class="section"><h2>진학 결과와 지원서비스는 구분해서 봅니다</h2><p class="lead">2025 학부 졸업생의 대학원 진학·취업 결과는 별도 전공·진로 페이지에서 확인할 수 있습니다. 이 페이지는 재학 중 이용할 수 있는 Career and Employability Service에 초점을 둡니다.</p></section>'''+related(("unnc-programmes-careers.html","전공·졸업 후 진로","2025 대학원 진학·취업 결과를 전공과 함께 확인합니다."),("unnc-exchange-study-abroad.html","교환학생·Study Abroad","글로벌 경험과 커리어 준비를 연결해 봅니다.")),
    [("UNNC는 1:1 취업 상담이 있나요?","커리어 staff, industry experts, headhunters, further study consultants, alumni 등 70명 이상의 adviser pool을 통한 1-to-1 career advice가 운영됩니다."),("인턴십 지원이 있나요?","Summer Placement Programme과 기업방문·교내 채용 활동 등을 통해 인턴십 및 취업 준비를 지원합니다."),("대학원 지원 상담도 받을 수 있나요?","Further Study Fair, 정보 세션, GRE·GMAT practice test, 1:1 further study advising과 application session이 운영됩니다.")],
    [("UNNC · Careers and Employability","https://www.nottingham.edu.cn/en/careers/"),("UNNC · International Student Guide 2026",P_GUIDE)]
)

# Replace the homepage internal-guides block with a broader related-articles hub.
index_path = ROOT / "index.html"
index = index_path.read_text(encoding="utf-8")
start = index.index("<!-- ===== INTERNAL GUIDES ===== -->")
end = index.index("<!-- ===== CALENDAR (TUITION) ===== -->")
new_guides = '''<!-- ===== INTERNAL GUIDES ===== -->
<section class="sec" id="guides">
  <div class="wrap">
    <div class="center">
      <span class="eyebrow" style="color:var(--gold-lt)">UNNC RELATED GUIDES</span>
      <h2 class="sec-title">UNNC 관련 글 · 상세 가이드</h2>
      <p class="sec-sub">메인페이지에서는 핵심만 보고, 입학·비용·학위·기숙사·교환학생·수업방식·진로·닝보 생활은 주제별 상세페이지에서 더 자세히 확인할 수 있습니다.</p>
    </div>
    <div class="guide-grid rv">
      <a class="guide-card" href="unnc-admission-requirements-korea-2027.html"><span class="gt">ADMISSION</span><h3>2027 한국학생 입학조건</h3><p>Year 1·Year 2, 한국 학력, IELTS·PTE·TOEFL과 전공별 조건을 정리했습니다.</p><span class="more">입학조건 자세히 →</span></a>
      <a class="guide-card" href="unnc-application-documents-2027.html"><span class="gt">APPLICATION</span><h3>지원서류·지원 준비</h3><p>성적표, 졸업증명, 추천서, Personal Statement, 여권과 증명사진을 체크합니다.</p><span class="more">지원 준비 자세히 →</span></a>
      <a class="guide-card" href="unnc-tuition-scholarships-2027.html"><span class="gt">COST</span><h3>학비·장학금·연간 비용</h3><p>학부 학비 120,000 RMB, 장학금과 원화 환산, 전체 예산을 비교합니다.</p><span class="more">비용 자세히 →</span></a>
      <a class="guide-card" href="unnc-accommodation-campus-life.html"><span class="gt">ACCOMMODATION</span><h3>기숙사·캠퍼스 생활</h3><p>11동·12B동·20동 비용과 방 구조, 보안·의료·생활편의 시설을 확인합니다.</p><span class="more">기숙사 자세히 →</span></a>
      <a class="guide-card" href="unnc-nottingham-degree-uk-campus.html"><span class="gt">DEGREE & UK</span><h3>노팅엄 학위·4+0·2+2</h3><p>University of Nottingham degree certificate와 영국 캠퍼스 학업 구조를 설명합니다.</p><span class="more">학위 구조 자세히 →</span></a>
      <a class="guide-card" href="unnc-exchange-study-abroad.html"><span class="gt">GLOBAL</span><h3>교환학생·Study Abroad</h3><p>Exchange, Study Abroad, Summer School의 기간과 학비 구조 차이를 정리했습니다.</p><span class="more">글로벌 기회 자세히 →</span></a>
      <a class="guide-card" href="unnc-how-study-english-teaching.html"><span class="gt">STUDY</span><h3>영어수업·수업방식</h3><p>15~20명 세미나, module, 평가, Personal Tutor와 학업지원 구조를 확인합니다.</p><span class="more">수업방식 자세히 →</span></a>
      <a class="guide-card" href="unnc-programmes-careers.html"><span class="gt">PROGRAMMES</span><h3>전공·졸업 후 진로</h3><p>경영·AI·공학·인문사회 전공과 2025 대학원·취업 결과를 함께 봅니다.</p><span class="more">전공·진로 자세히 →</span></a>
      <a class="guide-card" href="unnc-career-support-further-study.html"><span class="gt">CAREER SUPPORT</span><h3>취업·대학원 진학 지원</h3><p>인턴십, Career Week, 1:1 상담, 90개+ 워크숍과 대학원 지원 서비스를 정리했습니다.</p><span class="more">커리어 지원 자세히 →</span></a>
      <a class="guide-card" href="unnc-ningbo-china-life.html"><span class="gt">NINGBO LIFE</span><h3>닝보 유학생활·중국생활</h3><p>상하이 접근성, 교통, 음식, 생활환경과 중국에서 공부하는 의미를 확인합니다.</p><span class="more">닝보 생활 자세히 →</span></a>
    </div>
  </div>
</section>

'''
index_path.write_text(index[:start] + new_guides + index[end:], encoding="utf-8")

# Update sitemap with every distinct intent page.
sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://unnc-korea.netlify.app/</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-admission-requirements-korea-2027.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-application-documents-2027.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-tuition-scholarships-2027.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-accommodation-campus-life.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-nottingham-degree-uk-campus.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-exchange-study-abroad.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-how-study-english-teaching.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-programmes-careers.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-career-support-further-study.html</loc><lastmod>2026-09-02</lastmod></url>
  <url><loc>https://unnc-korea.netlify.app/unnc-ningbo-china-life.html</loc><lastmod>2026-09-02</lastmod></url>
</urlset>\n'''
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

# Extend the permanent tone check to every new guide.
tone_path = ROOT / "scripts" / "authoritative_tone.py"
tone = tone_path.read_text(encoding="utf-8")
needle = '    ROOT / "unnc-nottingham-degree-uk-campus.html",\n'
addition = needle + '    ROOT / "unnc-application-documents-2027.html",\n    ROOT / "unnc-accommodation-campus-life.html",\n    ROOT / "unnc-exchange-study-abroad.html",\n    ROOT / "unnc-how-study-english-teaching.html",\n    ROOT / "unnc-career-support-further-study.html",\n    ROOT / "unnc-ningbo-china-life.html",\n'
if 'unnc-application-documents-2027.html' not in tone:
    tone = tone.replace(needle, addition)
    tone_path.write_text(tone, encoding="utf-8")

print("Generated six UNNC detail guides, homepage related-guide links, sitemap, and tone-check coverage")
