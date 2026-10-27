(function () {
  'use strict';
  const deck = document.querySelector('.day-deck');
  if (!deck) return;
  const slides = Array.from(deck.querySelectorAll('.day-slide'));
  const controls = deck.querySelector('.day-controls');
  const chapters = deck.querySelector('.day-chapters');
  const status = deck.querySelector('#day-status');
  const play = deck.querySelector('[data-action="play"]');
  const prev = deck.querySelector('[data-action="prev"]');
  const next = deck.querySelector('[data-action="next"]');
  const staticButton = deck.querySelector('[data-action="static"]');
  const full = deck.querySelector('[data-action="full"]');
  const speed = deck.querySelector('#day-speed');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0, step = 3, playing = false, timer = null, isStatic = motion.matches;
  const total = 3;
  try { const saved = JSON.parse(sessionStorage.getItem('dh-day-20261027') || 'null'); if (saved && Number.isInteger(saved.index) && saved.index >= 0 && saved.index < slides.length) { index = saved.index; step = Math.max(0, Math.min(total, Number(saved.step) || 0)); } } catch (_) {}
  function stop() { playing = false; clearTimeout(timer); timer = null; play.textContent = '자동 재생'; }
  function schedule() {
    clearTimeout(timer);
    if (playing && !isStatic && !document.hidden) timer = setTimeout(() => advance(1, true), 5500 / Number(speed.value));
  }
  function render() {
    deck.classList.toggle('is-static', isStatic);
    slides.forEach((slide, i) => {
      slide.hidden = !isStatic && i !== index;
      slide.querySelectorAll('[data-step]').forEach(el => el.classList.toggle('is-future', i === index && Number(el.dataset.step) > step));
      slide.querySelector('.day-wire').style.strokeDashoffset = isStatic ? 0 : String(1 - step / total);
    });
    prev.disabled = isStatic || (index === 0 && step === 0);
    next.disabled = isStatic || (index === slides.length - 1 && step === total);
    play.disabled = isStatic;
    play.textContent = playing ? '일시정지' : '자동 재생';
    staticButton.setAttribute('aria-pressed', String(isStatic));
    staticButton.textContent = isStatic ? '발표 보기' : '정적 보기';
    chapters.querySelectorAll('button').forEach((b, i) => b.setAttribute('aria-current', String(i === index)));
    document.querySelectorAll('.day-return').forEach(a => a.setAttribute('href', '#slide-' + (index + 1)));
    try { sessionStorage.setItem('dh-day-20261027', JSON.stringify({index, step})); } catch (_) {}
    status.textContent = isStatic ? '정적 보기 · 모든 장 표시' : `${index + 1} / ${slides.length}장 · ${step} / ${total}단계${playing ? ' · 재생 중' : ''}`;
  }
  function revealSlide() {
    const header = document.querySelector('.site-header');
    const headerHeight = document.fullscreenElement || deck.classList.contains('day-expanded') ? 0 : header.getBoundingClientRect().height;
    slides[index].style.scrollMarginTop = Math.ceil(headerHeight + controls.offsetHeight + 16) + 'px';
    slides[index].scrollIntoView({block: 'start', behavior: 'auto'});
  }
  function saveHash() { history.replaceState(history.state, '', '#slide-' + (index + 1)); }
  function advance(direction, automatic) {
    if (isStatic) return;
    const previousIndex = index;
    if (!automatic) stop();
    if (direction > 0) {
      if (step < total) step++;
      else if (index < slides.length - 1) { index++; step = 0; }
      else stop();
    } else if (step > 0) step--;
    else if (index > 0) { index--; step = total; }
    if (index === slides.length - 1 && step === total) stop();
    saveHash(); render(); if (index !== previousIndex) revealSlide(); schedule();
  }
  function jump(i, focus) {
    stop(); index = Math.max(0, Math.min(slides.length - 1, i)); step = total;
    saveHash(); render();
    if (focus) { revealSlide(); slides[index].querySelector('h2').focus({preventScroll:true}); }
  }
  function syncHash() {
    const m = location.hash.match(/^#slide-(\d+)$/);
    if (m) jump(Number(m[1]) - 1, false);
  }
  controls.addEventListener('click', async e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.action === 'prev') advance(-1);
    if (b.dataset.action === 'next') advance(1);
    if (b.dataset.action === 'play') {
      if (playing) stop();
      else { if (index === slides.length - 1 && step === total) {index=0;step=0;} playing=true; schedule(); }
      render();
    }
    if (b.dataset.action === 'static') {stop();isStatic=!isStatic;render();}
    if (b.dataset.action === 'full') {
      stop(); render();
      if (deck.classList.contains('day-expanded')) {deck.classList.remove('day-expanded');document.body.style.overflow='';full.textContent='전체화면';}
      else if (document.fullscreenElement) { try {await document.exitFullscreen();} catch (_) {} }
      else {
        try {if (!deck.requestFullscreen) throw new Error('unsupported'); await deck.requestFullscreen();}
        catch (_) {deck.classList.add('day-expanded');document.body.style.overflow='hidden';full.textContent='화면 닫기';status.textContent='확대 보기 · 전체화면 미지원, Esc 또는 화면 닫기로 복귀';}
      }
    }
  });
  document.addEventListener('fullscreenchange', () => {full.textContent=document.fullscreenElement?'화면 닫기':'전체화면';});
  chapters.addEventListener('click', e => {const b=e.target.closest('[data-jump]');if(b)jump(Number(b.dataset.jump),true);});
  speed.addEventListener('change', schedule);
  document.addEventListener('keydown', e => {
    if (e.key==='Escape' && deck.classList.contains('day-expanded')) {full.click();return;}
    if (e.altKey || e.ctrlKey || e.metaKey || /INPUT|SELECT|TEXTAREA|BUTTON|A/.test(e.target.tagName) || e.target.isContentEditable || isStatic || !deck.getBoundingClientRect().bottom || deck.getBoundingClientRect().bottom < 0) return;
    if (e.key==='ArrowRight') {e.preventDefault();advance(1);}
    else if(e.key==='ArrowLeft') {e.preventDefault();advance(-1);}
    else if(e.key===' ') {e.preventDefault();play.click();}
    else if(e.key==='Home') {e.preventDefault();jump(0,true);}
    else if(e.key==='End') {e.preventDefault();jump(slides.length-1,true);}
  });
  let start = null;
  deck.querySelector('.day-stage').addEventListener('touchstart', e => {if(e.touches.length===1 && !e.target.closest('a,button'))start=[e.touches[0].clientX,e.touches[0].clientY];else start=null;},{passive:true});
  deck.querySelector('.day-stage').addEventListener('touchend', e => {if(!start)return;const t=e.changedTouches[0],dx=t.clientX-start[0],dy=t.clientY-start[1];start=null;if(Math.abs(dx)>65 && Math.abs(dx)>Math.abs(dy)*1.5)advance(dx<0?1:-1);},{passive:true});
  document.addEventListener('visibilitychange', () => {if(document.hidden){stop();render();}});
  window.addEventListener('pagehide', () => {stop();render();});
  window.addEventListener('pageshow', () => {stop();syncHash();render();});
  document.addEventListener('click', e => {
    const a=e.target.closest('a');if(!a)return;
    stop();render();
    const m=(a.getAttribute('href') || '').match(/^#slide-(\d+)$/);if(m)jump(Number(m[1])-1,false);
    if(deck.classList.contains('day-expanded'))full.click();
    if(document.fullscreenElement && !a.hash.startsWith('#slide-'))document.exitFullscreen().catch(()=>{});
  });
  window.addEventListener('hashchange', syncHash);
  motion.addEventListener('change', e => {if(e.matches){stop();isStatic=true;render();}});
  deck.classList.add('is-enhanced');controls.hidden=false;chapters.hidden=false;deck.querySelector('.day-help').hidden=false;syncHash();render();
})();
