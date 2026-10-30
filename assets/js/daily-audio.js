/* One pre-generated Korean audio track: its playback clock drives every slide. */
(function () {
  'use strict';
  const storageKey = 'dh-day-audio-' + (document.querySelector('.day-deck')?.dataset.date || location.pathname).replace(/-/g, '');
  window.createDailyAudio = function (options) {
    const audio = document.getElementById('day-audio');
    let cues = [], token = 0, state = 'ready', message = '한 번 시작하면 한국어 설명과 단계·다음 장이 자동 진행됩니다.', pendingSeek = null;
    try { const parsed = JSON.parse(document.getElementById('day-audio-cues').textContent); cues = Array.isArray(parsed) ? parsed : []; } catch (_) {}
    let failure = !audio || !cues.length;
    if (failure) return {
      available: false, enabled: false, state: 'error', ended: false, currentTime: 0,
      message: '이 날짜의 오디오가 준비되지 않았습니다. 정적 보기와 대본을 이용해 주세요.',
      start() {}, pause() {}, select() {}, rate() {}, setEnabled() {}, sync() {}
    };
    function change() { options.change(); }
    function position() {
      if (!cues.length || pendingSeek !== null) return;
      const time = audio.currentTime;
      try {sessionStorage.setItem(storageKey,String(time));} catch (_) {}
      let cue = cues[0];
      for (const candidate of cues) { if (candidate.start > time + 0.04) break; cue = candidate; }
      options.position(cue.slide, cue.step);
    }
    function fail(text) {
      token++; failure = true; state = 'error'; message = text;
      audio.pause(); options.state(false); change();
    }
    function seek(time) {
      pendingSeek = time;
      if (audio.readyState >= 1) { try {const target=Number.isFinite(audio.duration)?Math.min(time,audio.duration):time;if(!audio.seeking && Math.abs(audio.currentTime-target)<.02){pendingSeek=null;position();return;}audio.currentTime=target;} catch (_) {} }
    }
    try { const saved = Number(sessionStorage.getItem(storageKey)); if(Number.isFinite(saved) && saved > 0)pendingSeek=saved; } catch (_) {}
    audio.addEventListener('loadedmetadata', () => { if (pendingSeek !== null) seek(pendingSeek); position(); });
    audio.addEventListener('timeupdate', position);
    audio.addEventListener('seeked',()=>{if(audio.seeking)return;pendingSeek=null;position();});
    audio.addEventListener('playing', () => {
      if(audio.paused)return;
      if (document.hidden) { audio.pause(); return; }
      failure = false; state = 'playing'; message = audio.muted ? '음소거 · 오디오 시간에 맞춰 자동 진행 중' : '한국어 음성·단계·슬라이드 자동 진행 중';
      options.state(true); position(); change();
    });
    audio.addEventListener('pause', () => {
      if (!audio.paused) return;
      if (!failure && !audio.ended) {state = 'paused'; message = '일시정지 · 같은 위치에서 이어서 재생합니다.';}
      options.state(false); change();
    });
    audio.addEventListener('waiting', () => {if(!audio.paused){state='loading';message='오디오를 불러오는 중 · 재생 위치에서 대기합니다.';change();}});
    audio.addEventListener('ended', () => {state='ended';message='발표가 끝났습니다.';options.state(false);options.complete();change();});
    audio.addEventListener('error', () => fail('오디오를 불러오지 못했습니다. 기본 오디오 플레이어 또는 파일 링크와 대본을 이용해 주세요.'));
    audio.addEventListener('ratechange', change);
    audio.addEventListener('volumechange', () => {if(state==='playing')message=audio.muted?'음소거 · 자동 진행은 계속됩니다.':'한국어 음성·단계·슬라이드 자동 진행 중';change();});
    const api = {
      get available() { return !!cues.length; }, get enabled() { return !audio.muted; },
      get state() { return state; }, get message() { return message; }, get ended() {return audio.ended || state==='ended';},
      get currentTime() { return audio.currentTime; },
      start(rate) {
        const session = ++token; failure = false;
        if(audio.error){const resume=audio.currentTime||0;audio.load();pendingSeek=resume;}
        audio.playbackRate = rate;
        if (audio.ended || state==='ended') seek(0);
        state = 'loading'; message = '오디오 시작 확인 중'; options.state(true); change();
        // play() is called synchronously in the original user gesture, once for the
        // same continuous media element. No new play permission is needed per slide.
        let promise;
        try { promise = audio.play(); } catch (_) {fail('오디오를 시작하지 못했습니다. 아래 기본 플레이어의 재생 버튼을 눌러 주세요.');return;}
        if (promise && promise.catch) promise.catch(error => {
          if (session !== token) return;
          fail(error.name==='NotAllowedError' ? '브라우저가 재생을 막았습니다. 설정·음성의 기본 오디오 플레이어에서 재생을 눌러 주세요.' : '오디오 재생을 시작하지 못했습니다. 파일 연결과 기기 음량을 확인해 주세요.');
        });
      },
      pause() { token++; try {sessionStorage.setItem(storageKey,String(audio.currentTime));} catch (_) {} audio.pause(); if(state==='loading'){state='paused';message='일시정지 · 같은 위치에서 이어서 재생합니다.';options.state(false);change();} },
      select(slide, step) { token++; audio.pause(); const cue=cues.find(c=>c.slide===slide && c.step===Math.max(1,step)); if(cue)seek(cue.start); },
      rate(value) { audio.playbackRate=value; },
      setEnabled(value) {audio.muted=!value;change();},
      sync: position
    };
    setTimeout(()=>{if(pendingSeek!==null && audio.readyState>=1)seek(pendingSeek);if(audio.readyState>=1)position();change();},0);
    return api;
  };
})();
