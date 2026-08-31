#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
TODAY = "2026-09-01"
BASE = "https://unnc-korea.netlify.app"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Could not find expected block for {label}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, new_block: str, label: str) -> str:
    pattern = re.escape(start) + r".*?" + re.escape(end)
    if new_block in text:
        return text
    out, count = re.subn(pattern, new_block + "\n\n" + end, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Could not replace section {label}")
    return out


def page(title: str, description: str, path: str, eyebrow: str, h1: str, lead: str, hero_img: str, body: str, faq_json: str) -> str:
    canonical = f"{BASE}/{path}"
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="UNNC Korea | TNS유학">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{h1.replace('<br>',' ')}","description":"{description}","dateModified":"{TODAY}","mainEntityOfPage":"{canonical}","publisher":{{"@type":"Organization","name":"TNS유학 ㈜티앤에스월드와이드"}}}}</script>
<script type="application/ld+json">{faq_json}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/guide.css">
</head>
<body>
<div class="top">UNNC 한국어 입학 안내 · TNS유학</div>
<nav class="nav">
  <a class="brand" href="/">UNNC <span>Korea</span></a>
  <div class="navlinks"><a href="/">학교소개</a><a href="unnc-admission-requirements-korea-2027.html">입학조건</a><a href="unnc-tuition-scholarships-2027.html">학비·장학금</a><a href="unnc-programmes-careers.html">전공·진로</a><a href="unnc-nottingham-degree-uk-campus.html">학위·영국연계</a><a href="#contact">상담</a></div>
</nav>
<header class="hero" style="--hero-image:url('{hero_img}')">
  <div class="wrap"><div class="crumb"><a href="/">홈</a> › {eyebrow}</div><div class="eyebrow">{eyebrow}</div><h1>{h1}</h1><p>{lead}</p></div>
</header>
<main class="wrap">{body}</main>
<section class="cta" id="contact"><div class="wrap"><h2>UNNC 지원, 한국학생 기준으로 확인하세요</h2><p>학력·희망 전공·영어성적을 기준으로 Preliminary Year와 Qualifying Year 가능성을 함께 점검해 드립니다.</p><a class="btn" href="http://pf.kakao.com/_xfXsxjE" target="_blank" rel="noopener">카카오톡 상담</a><a class="btn alt" href="tel:0232881733">02-3288-1733</a></div></section>
<footer><div class="wrap">㈜티앤에스월드와이드 · 대표 신윤옥 · 사업자등록번호 220-87-54964<br>서울 강남구 테헤란로 5길 7 KG타워 B1 · 02-3288-1733 · tns@tnsuhak.com</div></footer>
</body>
</html>'''


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")

    # 1) Search/AI discovery metadata. Keep the existing visual design untouched.
    old_head = '''<title>노팅엄대학교 닝보 캠퍼스 한국 공식 안내 | UNNC Korea</title>
<meta name="description" content="영국 노팅엄대학교 닝보 캠퍼스(UNNC) 한국 공식 안내 — 100% 영어 강의, 영국 노팅엄과 동일한 학위, QS 세계 97위. TNS월드와이드 유학 안내.">'''
    new_head = '''<title>노팅엄대학교 닝보 캠퍼스(UNNC) 한국어 입학 안내 | 입학조건·학비·장학금 | TNS유학</title>
<meta name="description" content="노팅엄대학교 닝보 캠퍼스(UNNC) 한국어 입학 안내. University of Nottingham 동일 학위, 영어 전공교육, 국제학생 학부 학비 120,000위안. 한국학생 입학조건·장학금·전공·기숙사·진로 정보를 확인하세요.">
<meta name="author" content="TNS유학 ㈜티앤에스월드와이드">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://unnc-korea.netlify.app/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="UNNC Korea | TNS유학">
<meta property="og:title" content="노팅엄대학교 닝보 캠퍼스(UNNC) 한국어 입학 안내">
<meta property="og:description" content="University of Nottingham 동일 학위 · 영어 전공교육 · 한국학생 입학조건 · 학비·장학금 · 전공·진로 안내">
<meta property="og:url" content="https://unnc-korea.netlify.app/">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[{"@type":"WebSite","name":"UNNC Korea | TNS유학","url":"https://unnc-korea.netlify.app/","inLanguage":"ko-KR"},{"@type":"CollegeOrUniversity","name":"University of Nottingham Ningbo China","alternateName":"노팅엄대학교 닝보 캠퍼스 (UNNC)","url":"https://www.nottingham.edu.cn/en/","foundingDate":"2004","address":{"@type":"PostalAddress","streetAddress":"199 Taikang East Road","addressLocality":"Ningbo","addressRegion":"Zhejiang","addressCountry":"CN"}},{"@type":"Organization","name":"TNS유학 ㈜티앤에스월드와이드","url":"https://tnsuhak.com/","telephone":"+82-2-3288-1733","email":"tns@tnsuhak.com"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"UNNC 졸업장은 영국 노팅엄대학교와 같은가요?","acceptedAnswer":{"@type":"Answer","text":"UNNC 공식 안내에 따르면 영국, 중국, 말레이시아 캠퍼스에서 공부하는 University of Nottingham 학생은 같은 degree certificate를 받습니다."}},{"@type":"Question","name":"한국 고등학교 졸업생도 UNNC에 지원할 수 있나요?","acceptedAnswer":{"@type":"Answer","text":"가능합니다. 다만 South Korea 국가별 공식 기준은 학교 유형과 지원 학년에 따라 다르므로 Preliminary Year와 Qualifying Year 기준을 구분해 확인해야 합니다."}},{"@type":"Question","name":"UNNC 국제학생 학부 학비는 얼마인가요?","acceptedAnswer":{"@type":"Answer","text":"현재 UNNC 공식 학비 페이지의 국제학생 학부 학비는 연 120,000 RMB입니다. 기숙사와 생활비를 포함한 공식 연간 예상 총비용은 약 150,000~190,000 RMB입니다."}},{"@type":"Question","name":"UNNC 수업은 영어로 진행되나요?","acceptedAnswer":{"@type":"Answer","text":"UNNC 공식 글로벌 리크루팅 안내는 모든 degree programmes가 영어로 진행된다고 명시합니다."}},{"@type":"Question","name":"UNNC의 QS 세계 97위는 어떤 순위인가요?","acceptedAnswer":{"@type":"Answer","text":"97위는 University of Nottingham의 QS World University Rankings 2027 순위이며, UNNC 단독 세계대학 순위를 의미하지 않습니다."}}]}
</script>'''
    html = replace_once(html, old_head, new_head, "head metadata")

    # 2) Homepage factual corrections using current official UNNC sources.
    replacements = [
        ('<span class="badge"><span class="dot"></span>중국 최초 글로벌 대학교 · QS 세계 97위</span>', '<span class="badge"><span class="dot"></span>중국 최초 중외합작대학교 · 노팅엄대 QS 세계 97위</span>', 'hero badge'),
        ('<div class="hs"><div class="num">97<span class="u">위</span></div><div class="lab">QS 세계대학랭킹 2026</div></div>', '<div class="hs"><div class="num">97<span class="u">위</span></div><div class="lab">University of Nottingham · QS 2027</div></div>', 'ranking stat'),
        ('<div class="hs"><div class="num">47.7<span class="u">%</span></div><div class="lab">세계 TOP10 대학원 진학률</div></div>', '<div class="hs"><div class="num">47.7<span class="u">%</span></div><div class="lab">2025 대학원 진학생 · TOP10 오퍼</div></div>', 'graduate stat'),
        ('영국 노팅엄대학교 닝보 캠퍼스(UNNC)는 <span class="hi">2004년</span> 설립된, 영국 대학교가 중국에 세운 최초의 해외 캠퍼스입니다. 현재 70여 개국에서 온 약 <span class="hi">1만 명</span>의 학생이 재학 중이며, 글로벌 교수진이 100% 영어로 강의합니다.', '영국 노팅엄대학교 닝보 캠퍼스(UNNC)는 <span class="hi">2004년</span> 중국 교육부 승인을 받아 설립된 중국 최초의 중외합작대학교입니다. 현재 <span class="hi">1만 명 이상</span>의 학생이 재학하고, 학생과 교직원은 70개 이상의 국가·지역에서 모입니다. 모든 학위과정은 영어로 운영됩니다.', 'about paragraph 1'),
        ('영국 노팅엄대학교와 동일한 입학 기준·교육 품질·교수 채용 표준을 따르며, 영국·중국·말레이시아 세 캠퍼스 어디에서 졸업하더라도 <span class="hi">완전히 동일한 학위</span>를 받습니다. 하지만 유학비용은 영국에 비해 <span class="hi">1/3 수준</span>으로 매우 저렴합니다.', 'UNNC 공식 안내에 따르면 영국·중국·말레이시아의 University of Nottingham 학생은 졸업 시 <span class="hi">같은 degree certificate</span>를 받습니다. 닝보에서 영국식 고등교육을 경험하면서 중국어와 중국 비즈니스 환경을 함께 익힐 수 있다는 점이 특징입니다.', 'about paragraph 2'),
        ('학부 졸업생의 약 <span class="hi">47.7%</span>가 세계 TOP 10 대학원(하버드, 스탠포드, 예일, 옥스포드, 캠브릿지, 임페리얼, UCL, 홍콩, 싱가폴 등)에 진학합니다. 중국 본토에서 유일하게 QS Stars 전 9개 항목에서 <span class="hi">5스타(5 Stars)</span>를 획득했습니다.', '2024/25 Careers Report에 따르면 2025 학부 졸업생 가운데 대학원 진학을 선택한 학생의 <span class="hi">47.7%</span>가 세계 TOP 10 대학에서 오퍼를 받았고, 직접 취업한 학부 졸업생의 84% 이상이 Fortune Global 500·중국 Top 500·업계 선도기업·공공기관 등에 진출했습니다. UNNC는 <span class="hi">QS Stars 5-star institution</span>으로도 소개됩니다.', 'about paragraph 3'),
        ('<div class="fc"><div class="fnum">03</div><h3>경제적인 유학비용</h3><p>영국 노팅엄으로 유학가는 것에 비해 1/3 에 불과한 매우 저렴한 유학비용.</p></div>', '<div class="fc"><div class="fnum">03</div><h3>연 120,000 RMB</h3><p>현재 국제학생 학부 공식 학비. 기숙사·생활비까지 포함한 연간 예상 총비용도 함께 비교해야 합니다.</p></div>', 'feature tuition'),
        ('<div class="fc"><div class="fnum">04</div><h3>세계 TOP10 진학</h3><p>진학한 학부 졸업생의 약 47.7%가 세계 TOP10 대학원 석·박사 과정에 진학합니다.</p></div>', '<div class="fc"><div class="fnum">04</div><h3>TOP10 오퍼 47.7%</h3><p>2025 학부 졸업생 중 대학원 진학을 선택한 학생 기준으로 세계 TOP10 대학 오퍼 비율입니다.</p></div>', 'feature outcomes'),
        ('<li>170개 협력대학과 교환학생 운영 (추가 학비 없음)</li>', '<li>40개 이상 국가·지역의 160개 글로벌 파트너와 교환·Study Abroad 기회 운영</li>', 'partners'),
        ("<div><b>170<span style=\"font-size:1.2rem\">개</span></b><span>GLOBAL PARTNERS</span></div>", "<div><b>160<span style=\"font-size:1.2rem\">개</span></b><span>GLOBAL PARTNERS</span></div>", 'partner count'),
        ('<div><b>5★</b><span>QS STARS · 9개 항목</span></div>', '<div><b>5★</b><span>QS STARS INSTITUTION</span></div>', 'qs stars'),
        ('※ 환율 1 RMB = 220원 기준 · 영국 캠퍼스(2+2) 진학 학기는 영국 국제학생 학비 적용 · 국제학생 종합 의료·상해보험은 대학 부담', '※ 원화 환산은 1 RMB = 220원 가정치로 실제 환율에 따라 달라집니다. 국제학생의 공식 연간 예상 총비용은 학비·기숙사·보험·닝보 생활비를 포함해 약 150,000~190,000 RMB이며, 신입생은 원칙적으로 연간 학비를 전액 납부합니다.', 'tuition note'),
        ('<tr><td>닝보시/저장성 정부 장학금 (석사)</td><td>¥30,000</td></tr>\n          <tr><td>동문 장학금 (최대 3년)</td><td>15%</td></tr>\n          <tr><td>가족 장학금 (최대 4년)</td><td>10%</td></tr>', '<tr><td>저장성/닝보시 정부 장학금 (학부)</td><td>¥20,000</td></tr>\n          <tr><td>가족 장학금</td><td>10%</td></tr>', 'scholarship rows'),
        ('※ 장학 항목·금액은 변동될 수 있습니다. 자세한 내용은 TNS 상담 시 안내드립니다.', '※ Nottingham Global은 첫해 학비의 100%·50%·25% 장학입니다. 현재 공식 페이지의 2026 장학금 마감은 5월 31일이며, 2027 마감일은 공식 발표 후 업데이트합니다.', 'scholarship note'),
    ]
    for old, new, label in replacements:
        html = replace_once(html, old, new, label)

    # 3) Add an internal guide hub without changing the existing section design language.
    guide_css = '''
  /* ---------- INTERNAL GUIDES ---------- */
  #guides{background:#0e1a2e;color:#fff}
  #guides .sec-title{color:#fff}
  #guides .sec-sub{color:#c6d0de}
  .guide-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:34px}
  .guide-card{display:block;background:#fff;color:#24324a;border:1px solid rgba(255,255,255,.12);border-top:3px solid var(--gold);padding:25px 22px;min-height:190px;transition:.25s}
  .guide-card:hover{transform:translateY(-3px);box-shadow:0 18px 38px rgba(0,0,0,.22)}
  .guide-card .gt{font-family:'DM Mono',monospace;color:#9a7626;font-size:.66rem;letter-spacing:.12em}
  .guide-card h3{color:var(--navy);font-size:1.05rem;line-height:1.4;margin:9px 0}
  .guide-card p{color:#667085;font-size:.84rem;line-height:1.75}
  .guide-card .more{display:block;color:#8f6e22;font-weight:700;font-size:.82rem;margin-top:14px}
  @media(max-width:960px){.guide-grid{grid-template-columns:1fr 1fr}}
  @media(max-width:560px){.guide-grid{grid-template-columns:1fr}.guide-card{min-height:0}}
'''
    if guide_css not in html:
        html = html.replace('  /* ---------- FLOATING ---------- */', guide_css + '\n  /* ---------- FLOATING ---------- */', 1)

    guide_html = '''<!-- ===== INTERNAL GUIDES ===== -->
<section class="sec" id="guides">
  <div class="wrap">
    <div class="center">
      <span class="eyebrow" style="color:var(--gold-lt)">Korean Student Guides</span>
      <h2 class="sec-title">한국학생이 먼저 확인할 상세 가이드</h2>
      <p class="sec-sub">메인페이지에서는 핵심만 보고, 지원 판단에 필요한 조건·비용·전공·학위 구조는 주제별로 자세히 확인할 수 있습니다.</p>
    </div>
    <div class="guide-grid rv">
      <a class="guide-card" href="unnc-admission-requirements-korea-2027.html"><span class="gt">ADMISSION</span><h3>2027 UNNC 한국학생 입학조건</h3><p>South Korea 공식 기준, Preliminary Year·Qualifying Year, 영어성적과 2027 준비 포인트를 정리했습니다.</p><span class="more">입학조건 자세히 →</span></a>
      <a class="guide-card" href="unnc-tuition-scholarships-2027.html"><span class="gt">COST &amp; SCHOLARSHIP</span><h3>학비·장학금·기숙사비</h3><p>국제학생 학부 학비 120,000 RMB, 연간 예상 총비용과 Nottingham Global 장학금을 한 번에 비교합니다.</p><span class="more">비용 자세히 →</span></a>
      <a class="guide-card" href="unnc-programmes-careers.html"><span class="gt">PROGRAMMES &amp; CAREERS</span><h3>전공 선택과 졸업 후 진로</h3><p>경영·컴퓨터·공학·인문사회 전공과 2024/25 Careers Report의 대학원·취업 데이터를 함께 봅니다.</p><span class="more">전공·진로 자세히 →</span></a>
      <a class="guide-card" href="unnc-nottingham-degree-uk-campus.html"><span class="gt">DEGREE &amp; UK</span><h3>노팅엄 학위와 영국 캠퍼스</h3><p>같은 degree certificate의 의미, QS 97위의 정확한 대상, 일부 전공의 2+2 구조를 구분해 설명합니다.</p><span class="more">학위 구조 자세히 →</span></a>
    </div>
  </div>
</section>'''
    if guide_html not in html:
        html = html.replace('<!-- ===== CALENDAR (TUITION) ===== -->', guide_html + '\n\n<!-- ===== CALENDAR (TUITION) ===== -->', 1)

    # 4) Replace the unsupported Korean admission/deadline block with current official South Korea criteria.
    admission = '''<!-- ===== ADMISSION ===== -->
<section class="sec" id="admission" style="background:var(--cream)">
  <div class="wrap">
    <div class="center" style="margin-bottom:44px">
      <span class="eyebrow">Admission</span>
      <h2 class="sec-title">입학안내</h2>
      <p class="sec-sub">한국 지원자는 Preliminary Year(Year 1)과 Qualifying Year(Year 2)를 구분해 보는 것이 핵심입니다. 아래는 현재 UNNC가 공개한 South Korea 공식 기준을 바탕으로 정리했습니다.</p>
    </div>
    <div class="adm-grid">
      <div class="adm rv">
        <div class="anum">01</div><h3>Preliminary Year · Year 1</h3>
        <ul><li><span class="hl">South Korea 공식 대표 기준</span></li><li>- Specialized High School Diploma: 통상 80% 또는 B 이상</li><li>- Engineering Foundation 등 관련 과목이 필요한 경우 Maths·Physics 등도 80% 또는 B 이상</li><li>- 일반고·검정고시·기타 학력은 지원 전 개별 확인 권장</li></ul>
      </div>
      <div class="adm rv">
        <div class="anum">02</div><h3>Qualifying Year · Year 2</h3>
        <ul><li>- Foundation Programme 이수 또는 대학교 1년 이수</li><li>- 대표적인 최소 GPA 범위: 80% 또는 B 이상, 혹은 3.0~3.5 수준</li><li>- 전공별 필수과목과 직접 2학년 진입 가능 여부는 별도 확인</li></ul>
      </div>
      <div class="adm rv">
        <div class="anum">03</div><h3>영어 성적</h3>
        <ul><li><span class="hl">Preliminary Year:</span> IELTS 5.5, 각 영역 5.0 이상 / PTE 59, 각 53 이상</li><li><span class="hl">Qualifying Year:</span> IELTS 6.5, Writing 6.0 이상 / PTE 71, 각 65 이상</li><li>영문·항공우주 등 일부 전공은 별도 기준이 적용됩니다.</li></ul>
      </div>
      <div class="adm rv">
        <div class="anum">04</div><h3>2027 지원 준비</h3>
        <ul><li>현재 공식 사이트에는 2027 국제학생 지원·장학금 최종 마감일이 아직 게시되지 않았습니다.</li><li>2026 Nottingham Global 장학금 마감은 5월 31일이었으므로, 2027 일정은 발표 즉시 다시 확인해야 합니다.</li><li>성적표·졸업/재학증명·영어성적과 지원 전공의 과목요건을 먼저 준비하세요.</li></ul>
      </div>
      <div class="adm rv" style="grid-column:1/-1">
        <h3>지원 전 가장 많이 틀리는 부분</h3>
        <div class="detail-table"><table><tr><th>한국 내신</th><td>기존의 ‘내신 3~4등급’ 같은 비공식 컷은 공식 최소조건으로 사용하지 않습니다. 학교 유형과 학력에 따라 South Korea 기준을 적용해 확인합니다.</td></tr><tr><th>2027 마감일</th><td>공식 발표 전에는 임의의 날짜를 확정해서 안내하지 않습니다. 장학금과 일반 지원 마감도 서로 다를 수 있습니다.</td></tr><tr><th>영어조건</th><td>전공별 예외가 있으므로 최종 지원 전 해당 programme의 최신 prospectus를 다시 확인합니다.</td></tr></table></div>
        <p class="note"><a href="unnc-admission-requirements-korea-2027.html" style="color:#8d6b21;font-weight:700">→ 2027 한국학생 입학조건 상세 가이드 보기</a></p>
      </div>
    </div>
  </div>
</section>'''
    html = replace_between(html, '<!-- ===== ADMISSION ===== -->', '<!-- ===== REVIEWS ===== -->', admission, 'admission')

    INDEX.write_text(html, encoding="utf-8")

    # Shared styles for four search-intent detail pages.
    css = '''
:root{--navy:#14213d;--navy2:#0e1a2e;--gold:#c9a84c;--cream:#faf8f4;--ink:#151515;--mid:#667085;--rule:#e4e7ec;--white:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:'Noto Sans KR',sans-serif;color:var(--ink);background:var(--cream);line-height:1.78;word-break:keep-all}a{color:inherit}.wrap{width:min(1080px,90vw);margin:auto}.top{background:var(--navy2);color:#d7dce6;font-size:12px;padding:8px 5vw}.nav{height:68px;background:#fff;border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between;padding:0 5vw;position:sticky;top:0;z-index:10}.brand{font-size:22px;font-weight:900;color:var(--navy);text-decoration:none}.brand span{color:var(--gold)}.navlinks{display:flex;gap:19px}.navlinks a{color:var(--navy);font-size:12px;text-decoration:none;font-weight:700}.hero{position:relative;min-height:410px;color:#fff;display:flex;align-items:center;background:linear-gradient(105deg,rgba(10,18,38,.94),rgba(10,18,38,.64)),var(--hero-image) center/cover}.crumb{font-size:12px;color:rgba(255,255,255,.65);margin-bottom:24px}.crumb a{color:inherit}.eyebrow{font-family:'DM Mono',monospace;color:var(--gold);font-size:11px;letter-spacing:.16em}.hero h1{font-size:clamp(34px,5vw,58px);line-height:1.18;margin:12px 0 18px;max-width:900px}.hero p{font-size:17px;color:rgba(255,255,255,.8);max-width:800px}main{padding:70px 0}.section{margin-bottom:64px}.section h2{font-size:30px;line-height:1.35;color:var(--navy);margin:0 0 12px}.section h3{color:var(--navy)}.lead{color:var(--mid);max-width:850px;margin:0 0 28px}.answer{background:#fff;border-left:4px solid var(--gold);padding:24px 26px;margin-bottom:34px}.answer strong{color:var(--navy)}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:#fff;border:1px solid var(--rule);padding:27px}.card h3{margin:0 0 10px;font-size:18px}.card p,.card li{font-size:14px;color:#4b5565}.card ul{padding-left:20px}.tag{display:inline-block;font-family:'DM Mono',monospace;color:#8a6b20;background:#f7efd8;font-size:11px;padding:4px 8px;margin-bottom:12px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.stat{background:#fff;border:1px solid var(--rule);padding:24px}.stat b{display:block;color:var(--navy);font-size:30px;line-height:1.15}.stat span{font-size:12px;color:var(--mid)}.notice{background:#fff8e8;border-left:4px solid var(--gold);padding:20px 22px;color:#66562c;font-size:14px}.table-wrap{overflow:auto;background:#fff;border:1px solid var(--rule)}table{width:100%;border-collapse:collapse;min-width:680px}th,td{padding:15px 17px;border-bottom:1px solid var(--rule);text-align:left;font-size:13px;vertical-align:top}th{background:var(--navy);color:#fff}.faq details{background:#fff;border-bottom:1px solid var(--rule);padding:18px 22px}.faq summary{font-weight:800;color:var(--navy);cursor:pointer}.faq p{font-size:14px;color:#596273}.sources{border-top:1px solid var(--rule);padding-top:15px;color:#8a94a3;font-size:12px;line-height:1.8}.sources a{color:#667085;text-decoration:underline;text-underline-offset:2px}.cta{background:var(--navy);color:#fff;padding:52px 0;text-align:center}.cta h2{font-size:30px;margin:0 0 10px}.cta p{color:#d6deea}.btn{display:inline-block;margin:8px 5px 0;padding:13px 24px;background:#fee500;color:#161000;text-decoration:none;font-weight:800}.btn.alt{background:#fff;color:var(--navy)}footer{padding:34px 0;background:#0a0d18;color:#9ca3af;font-size:12px}
@media(max-width:820px){.navlinks{display:none}.hero{min-height:440px}.grid,.grid3,.stats{grid-template-columns:1fr 1fr}.hero h1{font-size:36px}}@media(max-width:560px){.grid,.grid3,.stats{grid-template-columns:1fr}.hero{min-height:430px}.hero p{font-size:15px}.section h2{font-size:25px}.card{padding:22px}.table-wrap{margin-left:-5vw;margin-right:-5vw}.cta{padding:42px 5vw}}
'''
    (ROOT / 'assets' / 'guide.css').write_text(css.strip() + '\n', encoding='utf-8')

    admission_body = '''
<section class="section"><div class="answer"><strong>핵심 답변:</strong> UNNC는 한국 지원자에게 Preliminary Year(Year 1)과 Qualifying Year(Year 2)를 별도로 안내합니다. 현재 South Korea 공식 페이지는 Preliminary Year의 대표 기준으로 Specialized High School Diploma 80% 또는 B 이상을 제시하고, Qualifying Year는 Foundation Programme 또는 대학 1년 이수를 요구합니다. 2027 최종 마감일은 아직 공식 공지 전입니다.</div><div class="stats"><div class="stat"><b>80% / B</b><span>South Korea · Preliminary Year 대표 기준</span></div><div class="stat"><b>1년</b><span>대학교 이수 후 Year 2 검토</span></div><div class="stat"><b>IELTS 5.5</b><span>Year 1 · 각 5.0 이상</span></div><div class="stat"><b>IELTS 6.5</b><span>Year 2 · Writing 6.0 이상</span></div></div></section>
<section class="section"><h2>한국학생 학력 기준</h2><p class="lead">UNNC 공식 South Korea 페이지에 공개된 문구를 그대로 기준점으로 삼고, 그 밖의 학력은 임의의 한국 내신 등급으로 환산하지 않습니다.</p><div class="grid"><article class="card"><span class="tag">PRELIMINARY YEAR</span><h3>Year 1</h3><ul><li>Specialized High School Diploma: 통상 80% 또는 B 이상</li><li>Engineering Foundation 등 관련 전공은 Maths·Physics 등 관련 과목도 80% 또는 B 이상</li><li>일반고·검정고시·기타 학력은 공식 페이지에 동일한 숫자 기준이 별도로 적혀 있지 않아 개별 확인이 필요</li></ul></article><article class="card"><span class="tag">QUALIFYING YEAR</span><h3>Year 2</h3><ul><li>Foundation Programme을 성공적으로 이수했거나 대학 1년 이수</li><li>대표 최소 GPA: 80% 또는 B 이상 또는 3.0~3.5 수준</li><li>지원 전공의 선수과목과 직접 진입 가능 여부는 programme별 확인</li></ul></article></div></section>
<section class="section"><h2>영어 조건</h2><div class="table-wrap"><table><thead><tr><th>구분</th><th>IELTS</th><th>PTE Academic</th><th>주의</th></tr></thead><tbody><tr><td>Preliminary Year</td><td>5.5, 각 5.0 이상</td><td>59, 각 53 이상</td><td>일부 전공은 별도 기준</td></tr><tr><td>Qualifying Year</td><td>6.5, Writing 6.0 이상</td><td>71, 각 65 이상</td><td>영어 관련 전공 등은 더 높은 기준 가능</td></tr></tbody></table></div><p class="notice">TOEFL 수치는 UNNC 공식 가이드와 일부 최신 course prospectus 사이에 표시 차이가 있어, 이 페이지에서는 고정 수치로 단정하지 않고 지원 전공의 최신 prospectus를 최종 확인하도록 안내합니다.</p></section>
<section class="section"><h2>2027 지원 준비</h2><div class="grid"><article class="card"><h3>지금 준비할 것</h3><p>고교/대학 성적표, 졸업·재학 상태, 영어성적, 지원 전공의 Maths·Physics 등 관련 과목 이수 여부를 먼저 정리하는 것이 효율적입니다.</p></article><article class="card"><h3>아직 확정하지 않을 것</h3><p>현재 공식 사이트에는 2027 국제학생 일반 지원과 장학금의 최종 마감일이 게시되지 않았습니다. 2026 Nottingham Global 장학금 마감은 5월 31일이었지만 2027에도 동일하다고 가정하지 않습니다.</p></article></div></section>
<section class="section faq"><h2>자주 묻는 질문</h2><details><summary>한국 일반고 학생은 지원이 안 되나요?</summary><p>그렇게 단정할 수 없습니다. 다만 현재 South Korea 공식 페이지가 숫자로 공개한 Preliminary Year 대표 기준은 Specialized High School Diploma 기준이므로 일반고 학력은 개별 확인이 필요합니다.</p></details><details><summary>내신 3~4등급이면 합격 가능한가요?</summary><p>UNNC 공식 최소조건으로 ‘내신 3~4등급’이 공개돼 있지 않으므로 공식 컷처럼 안내하지 않습니다.</p></details><details><summary>대학 1년을 다니면 바로 2학년으로 갈 수 있나요?</summary><p>Year 2 검토의 기본 조건이 될 수 있지만 GPA, 선수과목, 전공별 기준을 함께 충족해야 합니다.</p></details></section>
<section class="section sources"><strong>자료 출처</strong><br><a href="https://www.nottingham.edu.cn/en/Study-with-us/Undergraduate/Entry-requirements/International-applicants.aspx?country=South+Korea&level=Undergraduate" target="_blank" rel="noopener">UNNC · South Korea undergraduate entry requirements</a><br><a href="https://www.nottingham.edu.cn/en/study-with-us/undergraduate/entry-requirements/international.aspx" target="_blank" rel="noopener">UNNC · International applicants</a><br><a href="https://20anniversary.nottingham.edu.cn/documents/Student-Recruitment/International-student-guide-2026.pdf" target="_blank" rel="noopener">UNNC · International Student Guide 2026</a></section>'''
    admission_faq = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"한국 일반고 학생도 UNNC에 지원할 수 있나요?","acceptedAnswer":{"@type":"Answer","text":"지원 가능성은 있으나 현재 South Korea 공식 페이지가 숫자로 공개한 Preliminary Year 대표 기준은 Specialized High School Diploma 기준이므로 일반고 학력은 개별 확인이 필요합니다."}},{"@type":"Question","name":"UNNC Year 1 영어조건은 무엇인가요?","acceptedAnswer":{"@type":"Answer","text":"일반적인 Preliminary Year 최소 영어조건은 IELTS 5.5, 각 영역 5.0 이상 또는 PTE Academic 59, 각 53 이상입니다."}},{"@type":"Question","name":"UNNC Year 2는 대학 1년 이수 후 지원할 수 있나요?","acceptedAnswer":{"@type":"Answer","text":"South Korea 공식 기준은 Foundation Programme 또는 대학 1년 이수를 요구하며 대표 최소 GPA는 80% 또는 B 이상 혹은 3.0~3.5 수준입니다."}}]}'
    (ROOT / 'unnc-admission-requirements-korea-2027.html').write_text(page('UNNC 입학조건 2027 준비 | 한국학생 Year 1·Year 2·영어조건 | TNS유학','노팅엄대학교 닝보 캠퍼스(UNNC) 한국학생 입학조건. South Korea 공식 기준, Preliminary Year·Qualifying Year, IELTS/PTE와 2027 지원 준비를 정리했습니다.','unnc-admission-requirements-korea-2027.html','ADMISSION GUIDE','UNNC 입학조건<br>2027 한국학생 준비','한국 학력으로 어느 학년에 지원할 수 있는지, 공식 South Korea 기준과 영어조건을 분리해 확인합니다.','assets/embedded/886d437bcaf03f35.webp',admission_body,admission_faq),encoding='utf-8')

    tuition_body = '''
<section class="section"><div class="answer"><strong>핵심 답변:</strong> 현재 UNNC 공식 학비 페이지의 국제학생 학부 학비는 연 120,000 RMB입니다. 캠퍼스 기숙사는 연 11,000~20,000 RMB이며, 학비·기숙사·보험·닝보 생활비를 포함한 공식 예상 총비용은 연 약 150,000~190,000 RMB입니다.</div><div class="stats"><div class="stat"><b>120,000</b><span>RMB · 국제학생 학부 연 학비</span></div><div class="stat"><b>11k~20k</b><span>RMB · 연 기숙사비</span></div><div class="stat"><b>150k~190k</b><span>RMB · 공식 연간 총비용 추정</span></div><div class="stat"><b>최대 100%</b><span>Nottingham Global 첫해 장학</span></div></div></section>
<section class="section"><h2>학비와 실제 예산</h2><div class="table-wrap"><table><thead><tr><th>항목</th><th>현재 공식 기준</th><th>확인 포인트</th></tr></thead><tbody><tr><td>국제학생 학부 학비</td><td>120,000 RMB / year</td><td>일부 2+2 과정에서 영국 캠퍼스에 있는 기간은 당시 UK international fee 적용</td></tr><tr><td>국제학생 대학원 학비</td><td>대부분 130,000 RMB / year</td><td>특정 과정은 별도 학비</td></tr><tr><td>기숙사</td><td>11,000~20,000 RMB / academic year</td><td>객실 유형에 따라 차이</td></tr><tr><td>학부 연간 총비용</td><td>약 150,000~190,000 RMB</td><td>학비·기숙사·의무보험·닝보 생활비 포함, 장학금 제외</td></tr></tbody></table></div><p class="notice">신입생은 원칙적으로 연간 학비를 전액 납부해야 하며, commencing students에는 일반적인 분납제가 제공되지 않는다고 공식 페이지가 안내합니다.</p></section>
<section class="section"><h2>Nottingham Global 장학금</h2><div class="grid3"><article class="card"><span class="tag">FULL</span><h3>첫해 학비 100%</h3><p>Qualifying Year 기준 대표 최소 성취: A Level AAA 또는 IB 36 등. 입학 시 학업성취를 바탕으로 경쟁 선발됩니다.</p></article><article class="card"><span class="tag">HALF</span><h3>첫해 학비 50%</h3><p>대표 최소 성취: A Level AAB 또는 IB 34 등.</p></article><article class="card"><span class="tag">QUARTER</span><h3>첫해 학비 25%</h3><p>대표 최소 성취: A Level ABB 또는 IB 32 등.</p></article></div><p class="lead">최소 기준 충족이 장학금 수여를 보장하는 것은 아닙니다. Preliminary Year는 iGCSE 또는 equivalent 기준을 별도로 사용합니다.</p></section>
<section class="section"><h2>그 밖의 장학금</h2><div class="grid"><article class="card"><h3>Zhejiang/Ningbo Government Scholarship</h3><p>국제학생 학부 기준 20,000 RMB를 첫해 학비에 사용할 수 있는 장학금입니다.</p></article><article class="card"><h3>Family Scholarship</h3><p>UNNC의 등록 학생 또는 졸업생과 지정 가족관계에 해당할 경우 10% 학비 감면. 공식 페이지는 최대 4년까지 가능하다고 안내합니다.</p></article></div><p class="notice">현재 공식 페이지의 2026 장학금 제출 마감은 5월 31일입니다. 2027 마감일은 아직 공식 발표 전이므로 동일 날짜를 미리 확정하지 않습니다.</p></section>
<section class="section faq"><h2>자주 묻는 질문</h2><details><summary>학부 1년 총비용은 120,000 RMB인가요?</summary><p>아닙니다. 120,000 RMB는 학비이며, 공식 예상 총비용은 기숙사·보험·생활비를 포함해 약 150,000~190,000 RMB입니다.</p></details><details><summary>장학금 100%면 4년 전액인가요?</summary><p>Nottingham Global undergraduate full scholarship은 첫해 학비 100%에 해당합니다.</p></details><details><summary>영국 2+2 기간에도 중국 학비를 내나요?</summary><p>아닙니다. 해당 과정에서 영국 캠퍼스에서 공부하는 기간은 당시 University of Nottingham UK의 국제학생 학비가 적용됩니다.</p></details></section>
<section class="section sources"><strong>자료 출처</strong><br><a href="https://www.nottingham.edu.cn/en/study-with-us/undergraduate/fees-and-scholarships/" target="_blank" rel="noopener">UNNC · Undergraduate Fees and Scholarships</a><br><a href="https://www.nottingham.edu.cn/en/study-with-us/undergraduate/fees-and-scholarships/international.aspx" target="_blank" rel="noopener">UNNC · International Student Scholarships</a></section>'''
    tuition_faq = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"UNNC 국제학생 학부 학비는 얼마인가요?","acceptedAnswer":{"@type":"Answer","text":"현재 공식 기준 연 120,000 RMB입니다."}},{"@type":"Question","name":"UNNC의 연간 총비용은 얼마인가요?","acceptedAnswer":{"@type":"Answer","text":"학비, 기숙사, 의무보험, 닝보 생활비를 포함한 공식 추정치는 약 150,000~190,000 RMB입니다."}},{"@type":"Question","name":"Nottingham Global Full Scholarship은 몇 년 장학인가요?","acceptedAnswer":{"@type":"Answer","text":"학부 Full Scholarship은 첫해 학비 100%에 해당하는 entry-based scholarship입니다."}}]}'
    (ROOT / 'unnc-tuition-scholarships-2027.html').write_text(page('UNNC 학비·장학금 2027 준비 | 기숙사·연간 총비용 | TNS유학','UNNC 국제학생 학부 학비 120,000 RMB, 기숙사 11,000~20,000 RMB, 연간 총비용 150,000~190,000 RMB와 Nottingham Global 장학금을 공식 기준으로 정리했습니다.','unnc-tuition-scholarships-2027.html','TUITION & SCHOLARSHIP','UNNC 학비·장학금<br>2027 준비','학비 숫자만 보지 않고 기숙사·생활비·장학금과 영국 2+2 기간의 비용 구조까지 함께 비교합니다.','assets/embedded/6702ac55ed7d1baf.webp',tuition_body,tuition_faq),encoding='utf-8')

    careers_body = '''
<section class="section"><div class="answer"><strong>핵심 답변:</strong> UNNC는 경영·금융, 컴퓨터·AI, 공학·건축, 과학, 인문·사회 분야의 학부 전공을 운영합니다. 2024/25 Careers Report의 2025 학부 졸업생 자료에서는 87.4%가 대학원 진학, 7.5%가 직접 취업을 선택했고, 대학원 진학자 중 47.7%가 세계 TOP10 대학 오퍼를 받았습니다.</div><div class="stats"><div class="stat"><b>87.4%</b><span>2025 학부 · further study</span></div><div class="stat"><b>47.7%</b><span>진학자 중 TOP10 대학 오퍼</span></div><div class="stat"><b>97.8%</b><span>진학자 중 TOP100 대학 오퍼</span></div><div class="stat"><b>84%+</b><span>직접 취업자 · 주요 기업/기관</span></div></div></section>
<section class="section"><h2>분야별 전공 보기</h2><div class="grid"><article class="card"><span class="tag">BUSINESS &amp; FINANCE</span><h3>경영·금융·데이터 경영</h3><p>Finance, Accounting and Management, International Business Management, International Business Economics, Financial Technology, Big Data Management and Applications, Management Science 등이 있습니다.</p></article><article class="card"><span class="tag">AI &amp; COMPUTING</span><h3>컴퓨터·AI</h3><p>Computer Science, Computer Science with Artificial Intelligence 등. 수학·프로그래밍 적성과 영국 2+2 선택 여부를 함께 확인해야 합니다.</p></article><article class="card"><span class="tag">ENGINEERING &amp; DESIGN</span><h3>공학·건축</h3><p>Aerospace, Chemical, Civil, Electrical and Electronic Engineering, Architecture, Architectural Environment Engineering 등.</p></article><article class="card"><span class="tag">HUMANITIES &amp; SOCIAL SCIENCES</span><h3>경제·영어·국제학</h3><p>Economics, International Economics and Trade, English 계열, International Communications Studies, International Studies 등 다양한 선택지가 있습니다.</p></article></div></section>
<section class="section"><h2>2026년에 추가된 전공도 확인</h2><p class="lead">UNNC는 2026 첫 모집 기준으로 BSc Financial Technology, BSc Management Science, BSc Big Data Management and Applications 등 신규 학부 프로그램을 공식 사이트에서 소개했습니다. 전공명만 보고 선택하기보다 커리큘럼·필수 수학과목·캠퍼스 이동 구조를 함께 비교하는 것이 좋습니다.</p></section>
<section class="section"><h2>졸업 후 진로 데이터는 이렇게 읽어야 합니다</h2><div class="table-wrap"><table><thead><tr><th>2025 Careers Report 지표</th><th>공식 수치</th><th>해석</th></tr></thead><tbody><tr><td>학부 졸업생 further study</td><td>87.4%</td><td>대학원 진학 비중이 매우 높은 학교 특성을 보여줍니다.</td></tr><tr><td>대학원 진학자 TOP10 오퍼</td><td>47.7%</td><td>전체 졸업생이 아니라 대학원 진학을 선택한 학부 졸업생 기준입니다.</td></tr><tr><td>TOP50 / TOP100 오퍼</td><td>86.7% / 97.8%</td><td>진학을 선택한 학부 졸업생 기준입니다.</td></tr><tr><td>직접 취업</td><td>7.5%</td><td>그중 84% 이상이 Fortune Global 500·중국 Top500·업계 선도기업·공공기관 등에 취업했다고 보고됩니다.</td></tr><tr><td>International/HMT graduates</td><td>26.2% Mainland / 73.8% overseas</td><td>국제·홍콩·마카오·대만 졸업생의 진학·취업 지역 분포입니다.</td></tr></tbody></table></div><p class="notice">이 통계는 특정 한국 학생의 취업이나 대학원 합격을 보장하는 수치가 아닙니다. 특히 일부 고용률 지표는 중국 Gaokao 모집 학부 졸업생 코호트를 대상으로 하므로 모집집단을 구분해 읽어야 합니다.</p></section>
<section class="section faq"><h2>자주 묻는 질문</h2><details><summary>UNNC는 대학원 진학용 학교인가요?</summary><p>2025 학부 졸업생 통계에서는 대학원 진학 비중이 87.4%로 높았습니다. 다만 직접 취업과 창업을 선택한 졸업생도 있습니다.</p></details><details><summary>컴퓨터·AI 전공이 가장 취업에 유리한가요?</summary><p>일률적으로 말하기 어렵습니다. 수학·프로그래밍 적성, 프로젝트·인턴십, 중국어·영어, 목표 취업국가를 함께 봐야 합니다.</p></details><details><summary>TOP10 47.7%는 전체 졸업생 기준인가요?</summary><p>아닙니다. 대학원 진학을 선택한 2025 학부 졸업생 가운데 TOP10 대학 오퍼를 받은 비율입니다.</p></details></section>
<section class="section sources"><strong>자료 출처</strong><br><a href="https://www.nottingham.edu.cn/en/course/list.aspx" target="_blank" rel="noopener">UNNC · All courses and programmes</a><br><a href="https://www.nottingham.edu.cn/en/careers/2025-careers-report.aspx" target="_blank" rel="noopener">UNNC · 2024/25 Careers and Employability Report</a><br><a href="https://www.nottingham.edu.cn/en/study-with-us/home.aspx" target="_blank" rel="noopener">UNNC · Study with us</a></section>'''
    careers_faq = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"UNNC 학부 졸업생은 대학원 진학을 많이 하나요?","acceptedAnswer":{"@type":"Answer","text":"2025 Careers Report에서 학부 졸업생의 87.4%가 further study를 선택했습니다."}},{"@type":"Question","name":"UNNC TOP10 대학원 47.7%는 전체 졸업생 기준인가요?","acceptedAnswer":{"@type":"Answer","text":"아닙니다. 대학원 진학을 선택한 2025 학부 졸업생 가운데 TOP10 대학 오퍼를 받은 비율입니다."}},{"@type":"Question","name":"UNNC에는 AI와 FinTech 전공이 있나요?","acceptedAnswer":{"@type":"Answer","text":"공식 과정 목록에 Computer Science with Artificial Intelligence와 Financial Technology 등이 포함돼 있습니다."}}]}'
    (ROOT / 'unnc-programmes-careers.html').write_text(page('UNNC 전공·졸업 후 진로 | 대학원 진학·취업 데이터 | TNS유학','UNNC 학부 전공을 경영·금융·AI·컴퓨터·공학·건축·인문사회 분야별로 보고, 2024/25 Careers Report의 대학원 진학과 취업 데이터를 정확한 모집집단과 함께 정리했습니다.','unnc-programmes-careers.html','PROGRAMMES & CAREERS','UNNC 전공과<br>졸업 후 진로','전공명만 나열하지 않고 어떤 분야를 공부하는지와 2025 졸업생 진학·취업 데이터를 함께 봅니다.','assets/embedded/0cddcf1b60ebd2e7.webp',careers_body,careers_faq),encoding='utf-8')

    degree_body = '''
<section class="section"><div class="answer"><strong>핵심 답변:</strong> UNNC 공식 글로벌 리크루팅 안내는 University of Nottingham의 UK·China·Malaysia 학생들이 같은 degree certificate를 받는다고 명시합니다. 다만 이것은 모든 캠퍼스의 입학조건·생활비·세부 커리큘럼이 완전히 동일하다는 뜻은 아닙니다.</div><div class="stats"><div class="stat"><b>Same</b><span>University of Nottingham degree certificate</span></div><div class="stat"><b>100%</b><span>degree programmes taught in English</span></div><div class="stat"><b>#97</b><span>University of Nottingham · QS 2027</span></div><div class="stat"><b>2+2</b><span>일부 전공에서 UK campus 선택 가능</span></div></div></section>
<section class="section"><h2>‘같은 학위’의 정확한 의미</h2><div class="grid"><article class="card"><h3>같은 degree certificate</h3><p>UNNC 공식 자료는 영국·중국·말레이시아 캠퍼스에서 공부하는 University of Nottingham 학생이 같은 degree certificate를 받는다고 설명합니다. 중국 캠퍼스만의 별도 학위증을 받는 구조로 설명하지 않습니다.</p></article><article class="card"><h3>같은 학교 = 모든 조건이 동일?</h3><p>아닙니다. 국가별 입학조건, 학비, 기숙사, 학사 운영과 일부 programme 구성은 캠퍼스별로 다를 수 있습니다. ‘같은 학위증’과 ‘모든 운영조건 동일’을 구분해야 합니다.</p></article></div></section>
<section class="section"><h2>QS 세계 97위는 UNNC 단독 순위가 아닙니다</h2><p class="lead">UNNC 공식 홈페이지는 University of Nottingham이 QS World University Rankings 2027에서 세계 97위라고 안내합니다. 따라서 한국어 사이트에서도 ‘UNNC 세계 97위’처럼 별도 기관 순위로 오해될 표현보다 <strong>‘University of Nottingham · QS 세계 97위(2027)’</strong>라고 표시하는 것이 정확합니다.</p></section>
<section class="section"><h2>2+2와 영국 캠퍼스</h2><div class="table-wrap"><table><thead><tr><th>구조</th><th>의미</th><th>비용</th></tr></thead><tbody><tr><td>4+0</td><td>학위과정을 닝보에서 이수하는 형태. 일부 과정에서 Study Abroad/Exchange 기회가 별도로 있을 수 있습니다.</td><td>UNNC 국제학생 학비 기준</td></tr><tr><td>2+2</td><td>일부 전공에서 마지막 2년을 University of Nottingham UK에서 공부하는 선택지</td><td>영국 캠퍼스 기간에는 당시 UK international fee 적용</td></tr></tbody></table></div><p class="notice">2+2 가능 여부는 전공별로 다릅니다. 지원 전에 해당 course prospectus에서 ‘2+2 / 4+0’ 구조를 확인해야 합니다.</p></section>
<section class="section"><h2>왜 이 구조가 한국학생에게 중요한가</h2><div class="grid3"><article class="card"><span class="tag">DEGREE</span><h3>졸업장 이해</h3><p>중국에서 공부한다는 이유만으로 별도의 중국 현지 학위로 보는 오해를 줄일 수 있습니다.</p></article><article class="card"><span class="tag">COST</span><h3>비용 계획</h3><p>닝보 4+0과 UK 2+2는 후반부 학비 구조가 크게 다를 수 있어 예산을 미리 나눠 봐야 합니다.</p></article><article class="card"><span class="tag">CAREER</span><h3>진학·취업</h3><p>영어 학위과정과 중국 경험을 어떻게 대학원·취업 목표에 연결할지 전공 선택 단계부터 설계할 수 있습니다.</p></article></div></section>
<section class="section faq"><h2>자주 묻는 질문</h2><details><summary>졸업장에 Ningbo가 따로 표시되나요?</summary><p>UNNC 공식 설명의 핵심은 세 캠퍼스 학생이 같은 degree certificate를 받는다는 것입니다. 개별 증명서 표기나 학적 증명 세부는 지원·졸업 시점의 공식 문서를 확인하는 것이 가장 정확합니다.</p></details><details><summary>UNNC 자체가 QS 97위인가요?</summary><p>아닙니다. 97위는 University of Nottingham의 QS World University Rankings 2027 순위입니다.</p></details><details><summary>모든 전공이 2+2 가능한가요?</summary><p>아닙니다. 일부 전공에만 제공되므로 course별 prospectus를 확인해야 합니다.</p></details></section>
<section class="section sources"><strong>자료 출처</strong><br><a href="https://www.nottingham.edu.cn/en/study-with-us/global-recruitment/home.aspx" target="_blank" rel="noopener">UNNC · Global recruitment</a><br><a href="https://www.nottingham.edu.cn/en/study-with-us/undergraduate/fees-and-scholarships/" target="_blank" rel="noopener">UNNC · Undergraduate fees</a><br><a href="https://www.nottingham.edu.cn/en/course/list.aspx" target="_blank" rel="noopener">UNNC · All courses and programmes</a><br><a href="https://www.nottingham.ac.uk/about/facts/rankings-and-achievements.aspx" target="_blank" rel="noopener">University of Nottingham · Rankings and achievements</a></section>'''
    degree_faq = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"UNNC 졸업장은 영국 노팅엄대학교와 같은가요?","acceptedAnswer":{"@type":"Answer","text":"UNNC 공식 글로벌 리크루팅 안내는 UK, China, Malaysia 학생이 같은 degree certificate를 받는다고 명시합니다."}},{"@type":"Question","name":"UNNC가 QS 세계 97위인가요?","acceptedAnswer":{"@type":"Answer","text":"97위는 University of Nottingham의 QS World University Rankings 2027 순위입니다."}},{"@type":"Question","name":"UNNC 모든 전공이 2+2인가요?","acceptedAnswer":{"@type":"Answer","text":"아닙니다. 2+2는 일부 전공에서 제공되며 course별 prospectus 확인이 필요합니다."}}]}'
    (ROOT / 'unnc-nottingham-degree-uk-campus.html').write_text(page('UNNC 졸업장·노팅엄 학위 | 영국 캠퍼스 2+2·QS 97위 정확히 보기 | TNS유학','UNNC 졸업장이 University of Nottingham과 어떻게 연결되는지, 같은 degree certificate의 의미, QS 세계 97위의 정확한 대상과 일부 전공의 2+2 구조를 설명합니다.','unnc-nottingham-degree-uk-campus.html','DEGREE & UK CAMPUS','UNNC 졸업장과<br>노팅엄대학교 학위','같은 degree certificate, QS 순위, 4+0·2+2를 서로 섞지 않고 정확히 구분해 봅니다.','assets/embedded/fb37d028ec91561a.webp',degree_body,degree_faq),encoding='utf-8')

    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://unnc-korea.netlify.app/sitemap.xml\n', encoding='utf-8')
    urls = ['', '/unnc-admission-requirements-korea-2027.html', '/unnc-tuition-scholarships-2027.html', '/unnc-programmes-careers.html', '/unnc-nottingham-degree-uk-campus.html']
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = BASE + ('/' if u == '' else u)
        sitemap.append(f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod></url>')
    sitemap.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sitemap) + '\n', encoding='utf-8')

    print('UNNC homepage fact/SEO upgrade applied')
    print('4 detail guides + shared CSS + robots + sitemap generated')


if __name__ == '__main__':
    main()
