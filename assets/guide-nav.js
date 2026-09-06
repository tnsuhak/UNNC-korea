(function(){
  var MENU_HTML = '' +
    '<div class="site-menu-inner">' +
      '<div class="site-menu-head">' +
        '<div class="site-menu-headcopy"><span>UNNC KOREA</span><h2>전체 메뉴</h2><p>메인 페이지의 주제와 관련 상세페이지를 함께 확인하세요.</p></div>' +
        '<button type="button" class="site-menu-close" aria-label="전체 메뉴 닫기">✕</button>' +
      '</div>' +
      '<div class="site-menu-grid">' +
        '<section class="site-menu-group"><h3><a href="/#information">학교소개 <small>메인에서 보기 →</small></a></h3><a href="/unnc-nottingham-degree-uk-campus.html">노팅엄 학위·영국 캠퍼스 연계</a><a href="/unnc-how-study-english-teaching.html">영어수업·수업방식</a></section>' +
        '<section class="site-menu-group"><h3><a href="/#major">전공안내 <small>메인에서 보기 →</small></a></h3><a href="/unnc-programmes-careers.html">전공·대학원 진학</a><a href="/unnc-career-support-further-study.html">취업·대학원 지원</a></section>' +
        '<section class="site-menu-group"><h3><a href="/#calendar">학비·장학금 <small>메인에서 보기 →</small></a></h3><a href="/unnc-tuition-scholarships-2027.html">2027 학비·장학금 상세</a></section>' +
        '<section class="site-menu-group"><h3><a href="/#rooms">숙소 <small>메인에서 보기 →</small></a></h3><a href="/unnc-accommodation-campus-life.html">기숙사·캠퍼스 생활</a><a href="/unnc-ningbo-china-life.html">닝보 유학생활</a></section>' +
        '<section class="site-menu-group"><h3><a href="/#campus">캠퍼스생활 <small>메인에서 보기 →</small></a></h3><a href="/unnc-sports-gym-fitness.html">스포츠·GYM 시설</a><a href="/unnc-clubs-student-organisations.html">동아리·학생단체</a><a href="/unnc-exchange-study-abroad.html">교환학생·Study Abroad</a></section>' +
        '<section class="site-menu-group"><h3><a href="/#admission">입학안내 <small>메인에서 보기 →</small></a></h3><a href="/unnc-admission-requirements-korea-2027.html">2027 한국학생 입학조건</a><a href="/unnc-application-documents-2027.html">지원서류 안내</a></section>' +
        '<section class="site-menu-group"><h3><a href="/#reviews">재학생후기 <small>메인에서 보기 →</small></a></h3><a href="/unnc-korean-student-reviews.html">UNNC 한국학생 후기 영상 모음</a></section>' +
        '<section class="site-menu-group"><h3><a href="/#inquiry">입학문의 <small>메인에서 보기 →</small></a></h3><p>입학조건·학비·전공·숙소 상담은 TNS유학에서 안내합니다.</p><div class="site-menu-cta"><a class="kakao" href="http://pf.kakao.com/_xfXsxjE" target="_blank" rel="noopener">카카오톡 상담</a><a class="phone" href="tel:0232881733">전화상담</a></div></section>' +
      '</div>' +
    '</div>';

  var CSS = '' +
    'html{scroll-padding-top:118px}' +
    '.nav-menu-btn{display:inline-flex;align-items:center;gap:8px;background:transparent;border:1px solid #d9dde6;color:#14213d;padding:9px 13px;border-radius:4px;font-family:\'Noto Sans KR\',sans-serif;font-size:13.5px;font-weight:700;cursor:pointer;white-space:nowrap;transition:.2s}' +
    '.nav-menu-btn:hover,.nav-menu-btn[aria-expanded="true"]{background:#14213d;color:#fff;border-color:#14213d}.nav-menu-icon{font-size:14px;font-weight:400;line-height:1}' +
    '.site-menu{display:none;position:fixed;left:0;right:0;z-index:1200;background:#fff;color:#262d40;border-top:1px solid rgba(20,33,61,.1);box-shadow:0 24px 55px rgba(10,18,34,.22);overflow-y:auto}.site-menu.open{display:block}' +
    '.site-menu-inner{max-width:1200px;margin:0 auto;padding:28px 40px 34px}.site-menu-head{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;padding-bottom:18px;border-bottom:1px solid #e4e7ec;background:#fff;color:#14213d}.site-menu-headcopy>span{display:block;color:#9a7827;font-family:\'DM Mono\',monospace;font-size:10px;font-weight:700;letter-spacing:.12em;margin-bottom:4px}.site-menu-head h2{font-family:\'Noto Sans KR\',sans-serif;font-size:25px;line-height:1.3;margin:0;color:#14213d}.site-menu-head p{margin:6px 0 0;color:#6a7283;font-size:13px}' +
    '.site-menu-close{border:1px solid #d9dde6;background:#fff;color:#14213d;width:38px;height:38px;border-radius:0;cursor:pointer;font-size:16px;line-height:1;flex:0 0 auto}.site-menu-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px 30px;padding-top:24px}.site-menu-group{min-width:0;padding:0;border:0}.site-menu-group h3{font-family:\'Noto Sans KR\',sans-serif;font-size:16px;color:#14213d;margin:0 0 7px;border-bottom:2px solid #14213d}.site-menu-group h3 a{display:flex;align-items:baseline;justify-content:space-between;gap:10px;text-decoration:none;color:#14213d;padding:0 2px 10px;font-weight:800}.site-menu-group h3 a:hover{color:#9a7827}.site-menu-group h3 small{font-family:\'Noto Sans KR\',sans-serif;font-size:10.5px;font-weight:700;color:#9a7827;white-space:nowrap}.site-menu-group>a{display:block;text-decoration:none;color:#4f596e;font-size:14px;padding:8px 2px;border-bottom:1px solid #eeeae1}.site-menu-group>a:hover{color:#9a7827}.site-menu-group>p{font-size:13px;line-height:1.65;color:#747c8c;margin:10px 2px 0}.site-menu-cta{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.site-menu-cta a{flex:1 1 120px;text-align:center;border:0;padding:10px 12px;font-weight:800;text-decoration:none}.site-menu-cta .kakao{background:#fee500;color:#161000}.site-menu-cta .phone{background:#14213d;color:#fff}' +
    '.site-ham{display:none!important;flex-direction:column;gap:5px;cursor:pointer;padding:6px;background:none;border:none;margin-left:12px}.site-ham span{display:block;width:24px;height:2px;background:#333;transition:.3s}.site-ham[aria-expanded="true"]{background:#14213d}.site-ham[aria-expanded="true"] span{background:#fff}' +
    '@media(max-width:1120px){.nav-menu-btn{padding:9px 10px;font-size:12.8px}.site-menu-inner{padding-left:28px;padding-right:28px}}' +
    '@media(max-width:960px){html{scroll-padding-top:68px}.nav-links,.navlinks{display:none!important}.nav-menu-btn{display:none!important}.site-ham{display:flex!important}.site-menu-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.site-menu-inner{padding:22px 20px 30px}}' +
    '@media(max-width:620px){.site-menu-grid{grid-template-columns:1fr;gap:22px}.site-menu-head h2{font-size:22px}.site-menu-head p{font-size:12px}}';

  function injectStyles(){
    if(document.getElementById('xjtluStyleSiteMenuCss')) return;
    var style=document.createElement('style');
    style.id='xjtluStyleSiteMenuCss';
    style.textContent=CSS;
    document.head.appendChild(style);
  }

  function init(){
    var mainNav=document.getElementById('navbar');
    var guideNav=document.querySelector('.nav');
    var nav=mainNav || guideNav;
    if(!nav || document.getElementById('siteMenu')) return;
    injectStyles();

    document.querySelectorAll('.guide-menu-btn,.guide-menu-panel').forEach(function(el){el.remove();});
    var legacyMobile=document.getElementById('mobileNav');
    if(legacyMobile) legacyMobile.style.setProperty('display','none','important');

    var desktopLinks=mainNav ? mainNav.querySelector('.nav-links') : guideNav.querySelector('.navlinks');
    if(desktopLinks){
      var menuBtn=document.createElement('button');
      menuBtn.type='button';
      menuBtn.className='nav-menu-btn';
      menuBtn.setAttribute('aria-controls','siteMenu');
      menuBtn.setAttribute('aria-expanded','false');
      menuBtn.innerHTML='전체 메뉴 <span class="nav-menu-icon">☰</span>';
      desktopLinks.appendChild(menuBtn);
    }

    var oldHam=mainNav ? mainNav.querySelector('.nav-ham') : null;
    var ham=document.createElement('button');
    ham.type='button';
    ham.className='nav-ham site-ham';
    ham.id='siteHam';
    ham.setAttribute('aria-label','전체 메뉴');
    ham.setAttribute('aria-controls','siteMenu');
    ham.setAttribute('aria-expanded','false');
    ham.innerHTML='<span></span><span></span><span></span>';
    if(oldHam) oldHam.replaceWith(ham); else nav.appendChild(ham);

    var menu=document.createElement('div');
    menu.id='siteMenu';
    menu.className='site-menu';
    menu.setAttribute('aria-label','UNNC Korea 전체 메뉴');
    menu.setAttribute('aria-hidden','true');
    menu.innerHTML=MENU_HTML;
    document.body.appendChild(menu);

    var menuBtn=document.querySelector('.nav-menu-btn');
    var closeBtn=menu.querySelector('.site-menu-close');

    function positionMenu(){
      var bottom=Math.max(0,Math.round(nav.getBoundingClientRect().bottom));
      menu.style.top=bottom+'px';
      menu.style.maxHeight='calc(100vh - '+bottom+'px)';
    }
    function setOpen(open){
      menu.classList.toggle('open',open);
      menu.setAttribute('aria-hidden',open?'false':'true');
      ham.setAttribute('aria-expanded',open?'true':'false');
      if(menuBtn){
        menuBtn.setAttribute('aria-expanded',open?'true':'false');
        var icon=menuBtn.querySelector('.nav-menu-icon');
        if(icon) icon.textContent=open?'✕':'☰';
      }
      if(open) positionMenu();
    }
    function toggle(){setOpen(!menu.classList.contains('open'));}
    if(menuBtn) menuBtn.addEventListener('click',function(e){e.stopPropagation();toggle();});
    ham.addEventListener('click',function(e){e.stopPropagation();toggle();});
    closeBtn.addEventListener('click',function(e){e.stopPropagation();setOpen(false);});
    menu.addEventListener('click',function(e){e.stopPropagation();if(e.target.closest('a'))setOpen(false);});
    document.addEventListener('click',function(){setOpen(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false);});
    window.addEventListener('resize',function(){if(menu.classList.contains('open'))positionMenu();});
    window.addEventListener('scroll',function(){if(menu.classList.contains('open'))positionMenu();},{passive:true});
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
