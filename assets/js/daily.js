(function () {
  'use strict';
  const deck = document.querySelector('.day-deck');
  if (!deck) return;
  const slides = Array.from(deck.querySelectorAll('.day-slide'));
  const controls = deck.querySelector('.day-controls'), chapters = deck.querySelector('.day-chapters');
  const stage = deck.querySelector('.day-stage'), status = deck.querySelector('#day-status');
  const play = deck.querySelector('[data-action="play"]'), prev = deck.querySelector('[data-action="prev"]'), next = deck.querySelector('[data-action="next"]');
  const staticButton = deck.querySelector('[data-action="static"]'), focusButton = deck.querySelector('[data-action="full"]');
  const closeButton = deck.querySelector('[data-action="close-focus"]'), nativeButton = deck.querySelector('[data-action="native"]');
  const focusbar = deck.querySelector('.day-focusbar'), settings = deck.querySelector('.day-options');
  const speed = deck.querySelector('#day-speed'), voiceButton = deck.querySelector('[data-action="voice"]');
  const voiceStatus = deck.querySelector('#day-voice-status'), scriptButton = deck.querySelector('[data-action="script"]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0, step = 3, playing = false, isStatic = motion.matches, scriptsOpen = false;
  let focused = false, returnY = 0, returnTarget = null, exitPending = false, lockedStyles = null;
  let savedInert = [], narrator, afterFocusClose = null, focusHasHistory = false;
  let lastHistoryWrite = 0, hashTimer = null, originalRootOverflow = '';
  const total = 3;
  try { const saved = JSON.parse(sessionStorage.getItem('dh-day-20261027') || 'null'); if (saved && Number.isInteger(saved.index) && saved.index >= 0 && saved.index < slides.length) { index = saved.index; step = Math.max(0, Math.min(total, Number(saved.step) || 0)); } } catch (_) {}
  function historyWrite(method, state, url) {
    try { history[method](state, '', url); lastHistoryWrite = Date.now(); return true; }
    catch (_) { return false; } // WebKit rate limits must never disable controls or closing.
  }
  function saveHash(immediate) {
    clearTimeout(hashTimer); hashTimer = null;
    const hash = '#slide-' + (index + 1);
    if (location.hash === hash) return;
    const delay = 300 - (Date.now() - lastHistoryWrite);
    if (!immediate && delay > 0) { hashTimer = setTimeout(() => saveHash(), delay); return; }
    historyWrite('replaceState', history.state, hash);
  }
  function stop() { playing = false; if (narrator) narrator.pause(); }
  function render() {
    deck.classList.toggle('is-static', isStatic);
    slides.forEach((slide, i) => {
      slide.hidden = !isStatic && i !== index;
      slide.querySelectorAll('[data-step]').forEach(el => el.classList.toggle('is-future', i === index && Number(el.dataset.step) > step));
      slide.querySelector('.day-wire').style.strokeDashoffset = isStatic ? 0 : String(1 - step / total);
    });
    prev.disabled = isStatic || (index === 0 && step <= 1);
    next.disabled = isStatic || (index === slides.length - 1 && step === total);
    play.disabled = !narrator || !narrator.available;
    play.textContent = playing ? '일시정지' : narrator && narrator.ended ? '처음부터 재생' : narrator && narrator.currentTime > 0 ? '이어서 재생' : '▶ 발표 시작';
    staticButton.setAttribute('aria-pressed', String(isStatic)); staticButton.textContent = isStatic ? '발표 보기' : '정적 보기';
    focusButton.setAttribute('aria-pressed', String(focused));
    chapters.querySelectorAll('button').forEach((b, i) => b.setAttribute('aria-current', String(i === index)));
    document.querySelectorAll('.day-return').forEach(a => a.setAttribute('href', '#slide-' + (index + 1)));
    try { sessionStorage.setItem('dh-day-20261027', JSON.stringify({index, step})); } catch (_) {}
    const audioState = narrator ? ' · ' + (narrator.state==='playing' ? (narrator.enabled?'음성 자동 진행':'음소거 자동 진행') : narrator.state==='loading'?'오디오 준비 중':narrator.state==='error'?'오디오 오류':narrator.state==='ended'?'발표 끝':'재생 대기') : '';
    status.textContent = isStatic ? '정적 보기 · 모든 장 표시' : `${index + 1} / ${slides.length}장 · ${step} / ${total}단계${audioState}`;
    if(narrator){voiceButton.disabled=false;voiceButton.textContent=narrator.enabled?'음소거':'음소거 해제';voiceButton.setAttribute('aria-pressed',String(!narrator.enabled));voiceStatus.textContent=narrator.message;}
  }
  function revealSlide() {
    if (focused) { stage.scrollTop = 0; return; }
    const header = document.querySelector('.site-header');
    slides[index].style.scrollMarginTop = Math.ceil((document.fullscreenElement ? 0 : header.getBoundingClientRect().height) + controls.offsetHeight + 12) + 'px';
    slides[index].scrollIntoView({block: 'start', behavior: 'auto'});
  }
  function advance(direction) {
    if (isStatic) return;
    const previousIndex = index;
    stop();

    if (direction > 0) {
      if (step < total) step++;
      else if (index < slides.length - 1) { index++; step = 1; }
      else stop();
    } else if (step > 1) step--;
    else if (index > 0) { index--; step = total; }
    if (index === slides.length - 1 && step === total) stop();
    if(narrator)narrator.select(index,step);
    saveHash(); render(); if (index !== previousIndex) revealSlide();
  }
  function jump(i, focus) {
    stop(); index = Math.max(0, Math.min(slides.length - 1, i)); step = total;
    if(narrator)narrator.select(index,1);
    saveHash(); render(); if (focus) { revealSlide(); slides[index].querySelector('h2').focus({preventScroll:true}); }
  }
  function syncHash() { const m = location.hash.match(/^#slide-(\d+)$/); if (m) jump(Number(m[1]) - 1, false); }
  if(window.createDailyAudio)narrator=window.createDailyAudio({
    change: render,
    state: active=>{playing=active;if(active)isStatic=false;render();},
    position: (slide,part)=>{const moved=index!==slide;index=slide;step=part;saveHash();render();if(moved)revealSlide();},
    complete: ()=>{playing=false;index=slides.length-1;step=total;saveHash();render();}
  });
  function positionOptions() {
    if (!settings.open) return;
    const box = settings.querySelector('summary').getBoundingClientRect();
    const height = window.visualViewport ? visualViewport.height : innerHeight;
    const width = window.visualViewport ? visualViewport.width : innerWidth;
    const top = Math.max(8, Math.min(box.bottom + 6, height - Math.min(390, height - 24) - 12));
    deck.style.setProperty('--day-options-top', Math.round(top) + 'px');
    deck.style.setProperty('--day-options-left', Math.round(Math.max(12, Math.min(box.right - 310, width - 322))) + 'px');
    deck.style.setProperty('--day-options-height', Math.floor(height - top - 12) + 'px');
  }
  settings.addEventListener('toggle', positionOptions);
  document.addEventListener('click', e => {if(settings.open && !settings.contains(e.target))settings.open=false;});
  function viewport() {
    if (window.visualViewport && visualViewport.scale === 1) {
      deck.style.setProperty('--day-vh', Math.round(visualViewport.height) + 'px');
      deck.style.setProperty('--day-vtop', '0px');
      deck.style.setProperty('--day-vwidth', Math.round(visualViewport.width) + 'px');
    } else { deck.style.removeProperty('--day-vh'); deck.style.removeProperty('--day-vtop'); deck.style.removeProperty('--day-vwidth'); }
    positionOptions();
  }
  function enterFocus() {
    render(); if (focused) return;
    returnY = window.scrollY; window.scrollTo(0, returnY); returnTarget = document.activeElement; focused = true; settings.open = false;
    lockedStyles = {position:document.body.style.position, top:document.body.style.top, width:document.body.style.width, overflow:document.body.style.overflow};
    originalRootOverflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = 'hidden'; document.body.style.overflow = 'hidden';
    savedInert = Array.from(document.querySelectorAll('.site-header,.site-footer,.day-index')).map(el => [el, el.inert]); savedInert.forEach(([el]) => {el.inert = true;});
    deck.classList.add('day-focused'); deck.setAttribute('role','dialog'); deck.setAttribute('aria-modal','true'); deck.setAttribute('aria-labelledby','day-focus-title'); focusbar.hidden = false;
    clearTimeout(hashTimer); focusHasHistory = historyWrite('pushState', Object.assign({}, history.state, {dhDayFocus:true}), location.href);
    viewport(); render(); stage.scrollTop = 0; closeButton.focus({preventScroll:true});
  }
  function leaveFocus(fromHistory, afterClose) {
    if(document.fullscreenElement === deck && document.exitFullscreen)document.exitFullscreen().catch(()=>{});
    if (afterClose) afterFocusClose = afterClose;
    stop();  if (!focused) return;
    focused = false; deck.classList.remove('day-focused'); deck.removeAttribute('role'); deck.removeAttribute('aria-modal'); deck.removeAttribute('aria-labelledby'); focusbar.hidden = true; settings.open = false;
    Object.assign(document.body.style, lockedStyles); document.documentElement.style.overflow = originalRootOverflow; savedInert.forEach(([el, value]) => {el.inert = value;});
    window.scrollTo(0, returnY); if (returnTarget && returnTarget.isConnected) returnTarget.focus({preventScroll:true}); render();
    if (!fromHistory && focusHasHistory && history.state && history.state.dhDayFocus) {exitPending = true;history.back();}
    else { clearTimeout(hashTimer); if(afterFocusClose){const action=afterFocusClose;afterFocusClose=null;action();} else saveHash(true); }
  }
  controls.addEventListener('click', async e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.action === 'prev') advance(-1);
    if (b.dataset.action === 'next') advance(1);
    if (b.dataset.action === 'play') {
      settings.open=false;
      if(playing)stop();
      else if(narrator){if(isStatic){isStatic=false;render();}enterFocus();narrator.start(Number(speed.value));}
      render();
    }
    if (b.dataset.action === 'static') {stop(); isStatic=!isStatic; settings.open=false; render();}
    if (b.dataset.action === 'full') enterFocus();
    if (b.dataset.action === 'voice' && narrator) {narrator.setEnabled(!narrator.enabled);render();}
    if (b.dataset.action === 'script') {scriptsOpen=!scriptsOpen;slides.forEach(s=>s.querySelector('.day-script').open=scriptsOpen);scriptButton.setAttribute('aria-pressed',String(scriptsOpen));scriptButton.textContent=scriptsOpen?'대본 접기':'대본 보기';settings.open=false;}
    if (b.dataset.action === 'native') {
      stop(); render(); settings.open=false;
      try { if(document.fullscreenElement)await document.exitFullscreen();else await deck.requestFullscreen(); }
      catch (_) { enterFocus(); }
    }
  });
  closeButton.addEventListener('click', () => leaveFocus(false));
  document.addEventListener('fullscreenchange', () => {nativeButton.textContent=document.fullscreenElement?'기기 전체화면 종료':'기기 전체화면';stop();render();});
  window.addEventListener('popstate', () => {if(focused)leaveFocus(true);else if(exitPending){exitPending=false;clearTimeout(hashTimer);if(afterFocusClose){const action=afterFocusClose;afterFocusClose=null;action();}else saveHash(true);}});
  chapters.addEventListener('click', e => {const b=e.target.closest('[data-jump]');if(b)jump(Number(b.dataset.jump),true);});
  speed.addEventListener('change',()=>{if(narrator)narrator.rate(Number(speed.value));render();});
  document.addEventListener('keydown', e => {
    if (e.key==='Escape' && focused) {e.preventDefault();leaveFocus(false);return;}
    if (e.key==='Tab' && focused) {
      const items = Array.from(deck.querySelectorAll('button:not(:disabled),select:not(:disabled),summary,a[href],[tabindex="0"]')).filter(el=>el.getClientRects().length && !el.closest('[hidden]'));
      const first=items[0],last=items[items.length-1];
      if(e.shiftKey && document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey && document.activeElement===last){e.preventDefault();first.focus();}
    }
    if (e.altKey || e.ctrlKey || e.metaKey || /INPUT|SELECT|TEXTAREA|BUTTON|A|SUMMARY/.test(e.target.tagName) || e.target.isContentEditable || isStatic || (!focused && deck.getBoundingClientRect().bottom < 0)) return;
    if (e.key==='ArrowRight') {e.preventDefault();advance(1);}
    else if(e.key==='ArrowLeft') {e.preventDefault();advance(-1);}
    else if(e.key===' ') {e.preventDefault();play.click();}
    else if(e.key==='Home') {e.preventDefault();jump(0,true);}
    else if(e.key==='End') {e.preventDefault();jump(slides.length-1,true);}
  });
  let start = null;
  stage.addEventListener('touchstart', e => {
    if(e.touches.length===1 && e.target.closest('.day-diagram') && !e.target.closest('a,button'))start=[e.touches[0].clientX,e.touches[0].clientY,stage.scrollTop];else start=null;
  },{passive:true});
  stage.addEventListener('touchend', e => {if(!start||!e.changedTouches.length)return;const t=e.changedTouches[0],dx=t.clientX-start[0],dy=t.clientY-start[1],scrolled=Math.abs(stage.scrollTop-start[2]);start=null;if(Math.abs(dx)>65 && Math.abs(dx)>Math.abs(dy)*1.5 && scrolled<12)advance(dx<0?1:-1);},{passive:true});
  stage.addEventListener('touchcancel',()=>{start=null;},{passive:true});
  document.addEventListener('visibilitychange', () => {if(document.hidden){stop();render();}});
  window.addEventListener('pagehide', () => {clearTimeout(hashTimer);stop();render();});
  window.addEventListener('pageshow', () => {stop();if(narrator && narrator.currentTime>0)narrator.sync();else syncHash();render();});
  function followLocalLink(url) {
    clearTimeout(hashTimer);
    if(url.pathname === location.pathname && url.search === location.search && url.hash) {
      historyWrite('replaceState', history.state, url.hash);
      const target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if(target){
        if(target.classList.contains('day-slide')) revealSlide();
        else target.scrollIntoView({block:'start',behavior:'auto'});
        if(!target.hasAttribute('tabindex'))target.setAttribute('tabindex','-1');
        target.focus({preventScroll:true});
      }
    } else location.assign(url.href);
  }
  // Run before the shared site's capture listener: its smooth scrolling must not
  // scroll the document behind the fixed focus view, particularly in WebKit.
  document.addEventListener('click', e => {
    if(e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey)return;
    const a=e.target.closest('a');if(!a)return;
    clearTimeout(hashTimer); stop();render();
    const url = new URL(a.href, location.href);
    const localAnchor = url.origin === location.origin && url.pathname === location.pathname && url.search === location.search && url.hash && a.closest('.day-deck,.day-index');
    const m=(a.getAttribute('href') || '').match(/^#slide-(\d+)$/);if(m)jump(Number(m[1])-1,false);
    if(focused || localAnchor) {
      e.preventDefault(); e.stopImmediatePropagation(); settings.open=false;
      if(url.origin !== location.origin) {window.open(url.href,'_blank','noopener,noreferrer');leaveFocus(false);}
      else if(focused)leaveFocus(false,()=>followLocalLink(url));
      else followLocalLink(url);
      return;
    }
    if(document.fullscreenElement && !a.hash.startsWith('#slide-'))document.exitFullscreen().catch(()=>{});
  }, true);
  window.addEventListener('hashchange', () => {if(!exitPending)syncHash();});
  motion.addEventListener('change', e => {if(e.matches){stop();isStatic=true;render();}});
  window.addEventListener('resize',viewport); window.addEventListener('orientationchange',()=>{stop();settings.open=false;viewport();render();});
  if(window.visualViewport){visualViewport.addEventListener('resize',viewport);visualViewport.addEventListener('scroll',viewport);}
  nativeButton.hidden=!(document.fullscreenEnabled && deck.requestFullscreen && matchMedia('(pointer: fine)').matches);
  deck.classList.add('is-enhanced');controls.hidden=false;chapters.hidden=false;deck.querySelector('.day-help').hidden=false;viewport();syncHash();render();
})();
