(function(){
  function init(){
    var nav=document.querySelector('.nav');
    if(!nav || document.querySelector('.guide-menu-btn')) return;
    var btn=document.createElement('button');
    btn.type='button';
    btn.className='guide-menu-btn';
    btn.setAttribute('aria-label','전체 메뉴');
    btn.setAttribute('aria-expanded','false');
    btn.setAttribute('aria-controls','guideSiteMenu');
    btn.innerHTML='<span></span><span></span><span></span>';
    nav.appendChild(btn);

    var panel=document.createElement('nav');
    panel.id='guideSiteMenu';
    panel.className='guide-menu-panel';
    panel.setAttribute('aria-label','UNNC 전체 메뉴');
    panel.innerHTML='<a href="/">홈</a><a href="unnc-admission-requirements-korea-2027.html">입학조건</a><a href="unnc-application-documents-2027.html">지원서류</a><a href="unnc-tuition-scholarships-2027.html">학비·장학금</a><a href="unnc-programmes-careers.html">전공·대학원 진학</a><a href="unnc-nottingham-degree-uk-campus.html">학위·영국연계</a><a href="unnc-accommodation-campus-life.html">기숙사·캠퍼스</a><a href="unnc-ningbo-china-life.html">닝보 유학생활</a><a href="unnc-how-study-english-teaching.html">수업방식</a><a href="unnc-exchange-study-abroad.html">교환학생·Study Abroad</a><a href="unnc-clubs-student-organisations.html">동아리·학생단체</a><a href="unnc-sports-gym-fitness.html">스포츠·GYM</a><a href="unnc-korean-student-reviews.html">한국학생 후기</a><a href="unnc-career-support-further-study.html">취업·대학원 지원</a><a href="http://pf.kakao.com/_xfXsxjE" target="_blank" rel="noopener" class="menu-kakao">카카오톡 상담 →</a>';
    document.body.appendChild(panel);

    function positionPanel(){ panel.style.top=Math.round(nav.getBoundingClientRect().bottom)+'px'; }
    function closeMenu(){ panel.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }
    function toggleMenu(){
      var opening=!panel.classList.contains('open');
      if(opening){ positionPanel(); panel.classList.add('open'); btn.setAttribute('aria-expanded','true'); }
      else closeMenu();
    }
    btn.addEventListener('click',function(e){e.stopPropagation();toggleMenu();});
    panel.addEventListener('click',function(e){e.stopPropagation(); if(e.target.closest('a')) closeMenu();});
    document.addEventListener('click',closeMenu);
    document.addEventListener('keydown',function(e){if(e.key==='Escape') closeMenu();});
    window.addEventListener('resize',function(){if(panel.classList.contains('open')) positionPanel();});
    window.addEventListener('scroll',function(){if(panel.classList.contains('open')) positionPanel();},{passive:true});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
