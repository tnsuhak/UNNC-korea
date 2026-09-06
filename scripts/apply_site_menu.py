from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

MENU_LINKS = '''<a href="/">홈</a><a href="unnc-admission-requirements-korea-2027.html">입학조건</a><a href="unnc-application-documents-2027.html">지원서류</a><a href="unnc-tuition-scholarships-2027.html">학비·장학금</a><a href="unnc-programmes-careers.html">전공·대학원 진학</a><a href="unnc-nottingham-degree-uk-campus.html">학위·영국연계</a><a href="unnc-accommodation-campus-life.html">기숙사·캠퍼스</a><a href="unnc-ningbo-china-life.html">닝보 유학생활</a><a href="unnc-how-study-english-teaching.html">수업방식</a><a href="unnc-exchange-study-abroad.html">교환학생·Study Abroad</a><a href="unnc-clubs-student-organisations.html">동아리·학생단체</a><a href="unnc-sports-gym-fitness.html">스포츠·GYM</a><a href="unnc-korean-student-reviews.html">한국학생 후기</a><a href="unnc-career-support-further-study.html">취업·대학원 지원</a><a href="http://pf.kakao.com/_xfXsxjE" target="_blank" rel="noopener" class="menu-kakao">카카오톡 상담 →</a>'''

# Shared guide navigation CSS
css_path = ROOT / 'assets' / 'guide.css'
css = css_path.read_text(encoding='utf-8')
marker = '/* GUIDE SITE MENU */'
if marker not in css:
    css += '''\n\n/* GUIDE SITE MENU */\n.navlinks a[href="#contact"]{display:none}\n.guide-menu-btn{display:flex;width:42px;height:42px;align-items:center;justify-content:center;flex-direction:column;gap:5px;margin-left:18px;padding:0;border:1px solid var(--rule);border-radius:3px;background:#fff;cursor:pointer;flex:0 0 auto}\n.guide-menu-btn span{display:block;width:22px;height:2px;background:var(--navy);transition:.2s}\n.guide-menu-btn[aria-expanded="true"] span:nth-child(1){transform:translateY(7px) rotate(45deg)}\n.guide-menu-btn[aria-expanded="true"] span:nth-child(2){opacity:0}\n.guide-menu-btn[aria-expanded="true"] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}\n.guide-menu-panel{display:none;position:fixed;right:5vw;width:min(390px,90vw);max-height:calc(100vh - 90px);overflow-y:auto;background:#fff;border:1px solid var(--rule);box-shadow:0 22px 55px rgba(14,26,46,.22);z-index:1000;padding:8px 0}\n.guide-menu-panel.open{display:block}\n.guide-menu-panel a{display:block;padding:12px 20px;color:var(--navy);font-size:13px;font-weight:700;text-decoration:none;border-bottom:1px solid #f0f2f5}\n.guide-menu-panel a:hover{background:#f8f6ef;color:#8a6b20}\n.guide-menu-panel .menu-kakao{margin:10px 12px 6px;padding:13px 16px;background:#fee500;color:#161000;text-align:center;border:0}\n@media(max-width:1100px){.navlinks{display:none}.nav{padding-left:5vw;padding-right:5vw}.guide-menu-panel{left:0;right:0;width:100%;max-height:calc(100vh - 68px);border-left:0;border-right:0}.guide-menu-panel a{padding:14px 5vw;font-size:14px}}\n'''
    css_path.write_text(css, encoding='utf-8')

# Shared guide navigation JS
js_path = ROOT / 'assets' / 'guide-nav.js'
js_path.write_text('''(function(){\n  function init(){\n    var nav=document.querySelector('.nav');\n    if(!nav || document.querySelector('.guide-menu-btn')) return;\n    var btn=document.createElement('button');\n    btn.type='button';\n    btn.className='guide-menu-btn';\n    btn.setAttribute('aria-label','전체 메뉴');\n    btn.setAttribute('aria-expanded','false');\n    btn.setAttribute('aria-controls','guideSiteMenu');\n    btn.innerHTML='<span></span><span></span><span></span>';\n    nav.appendChild(btn);\n\n    var panel=document.createElement('nav');\n    panel.id='guideSiteMenu';\n    panel.className='guide-menu-panel';\n    panel.setAttribute('aria-label','UNNC 전체 메뉴');\n    panel.innerHTML=''' + repr(MENU_LINKS) + ''';\n    document.body.appendChild(panel);\n\n    function positionPanel(){ panel.style.top=Math.round(nav.getBoundingClientRect().bottom)+'px'; }\n    function closeMenu(){ panel.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }\n    function toggleMenu(){\n      var opening=!panel.classList.contains('open');\n      if(opening){ positionPanel(); panel.classList.add('open'); btn.setAttribute('aria-expanded','true'); }\n      else closeMenu();\n    }\n    btn.addEventListener('click',function(e){e.stopPropagation();toggleMenu();});\n    panel.addEventListener('click',function(e){e.stopPropagation(); if(e.target.closest('a')) closeMenu();});\n    document.addEventListener('click',closeMenu);\n    document.addEventListener('keydown',function(e){if(e.key==='Escape') closeMenu();});\n    window.addEventListener('resize',function(){if(panel.classList.contains('open')) positionPanel();});\n    window.addEventListener('scroll',function(){if(panel.classList.contains('open')) positionPanel();},{passive:true});\n  }\n  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();\n})();\n''', encoding='utf-8')

# Attach the shared menu JS to all guide pages.
for html_path in ROOT.glob('unnc-*.html'):
    html = html_path.read_text(encoding='utf-8')
    if 'assets/guide.css' not in html or 'assets/guide-nav.js' in html:
        continue
    html = html.replace('</body>', '<script src="assets/guide-nav.js" defer></script>\n</body>')
    html_path.write_text(html, encoding='utf-8')

# Main page: remove Kakao from the top-right nav and use the existing hamburger as the site menu.
index_path = ROOT / 'index.html'
index = index_path.read_text(encoding='utf-8')
index = index.replace('.nav-ham{display:none;flex-direction:column;gap:5px;background:none;border:0;cursor:pointer;padding:6px}', '.nav-ham{display:flex;flex-direction:column;gap:5px;background:none;border:0;cursor:pointer;padding:6px;margin-left:16px}')
index = index.replace('#mobileNav{display:none;position:fixed;top:70px;left:0;right:0;background:var(--navy);z-index:999;padding:14px 0 22px;box-shadow:0 20px 40px rgba(0,0,0,.3)}', '#mobileNav{display:none;position:fixed;top:106px;left:auto;right:20px;width:min(420px,calc(100vw - 40px));max-height:calc(100vh - 126px);overflow-y:auto;background:var(--navy);z-index:999;padding:14px 0 22px;box-shadow:0 20px 40px rgba(0,0,0,.3)}')
index = index.replace('#mobileNav{top:60px}', '#mobileNav{top:60px;left:0;right:0;width:auto;max-height:calc(100vh - 60px)}')
index = index.replace('<a href="http://pf.kakao.com/_xfXsxjE" target="_blank" rel="noopener" class="btn-inq">카카오 상담</a>', '')
index = index.replace('aria-label="메뉴"', 'aria-label="전체 메뉴"')
index = re.sub(r'<nav id="mobileNav">.*?</nav>', '<nav id="mobileNav" aria-label="UNNC 전체 메뉴">' + MENU_LINKS + '</nav>', index, count=1, flags=re.S)
index_path.write_text(index, encoding='utf-8')

print('Applied UNNC site menu to main and guide pages.')
